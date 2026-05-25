import argparse
import os
import sys
import json
import warnings
import re
from openai import OpenAI
# POPRAWIONO: Import jawnego typu wiadomości dla biblioteki OpenAI
from openai.types.chat import ChatCompletionMessageParam

# Importy interfejsu wizualnego
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner

# Import lokalnej logiki wykonawczej
from call_function import call_function_local

base_url = os.environ.get("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1")
api_key = os.environ.get("LOCAL_LLM_API_KEY", "lm-studio")

client = OpenAI(
    base_url=base_url,
    api_key=api_key
)
console = Console()

SYSTEM_PROMPT = """
You are an advanced, stateful AI Agent with direct tool access to a local coding workspace.
You must solve the user's task using a step-by-step loop.

CRITICAL INSTRUCTION:
Your response MUST ALWAYS be a single, valid JSON object and nothing else. No conversational greetings, no explanations outside the JSON structure.

JSON RESPONSE FORMAT:
If you need to use a tool to get information, return this exact format:
{
    "thought": "Your reasoning about what to do next based on previous data",
    "tool_call": {
        "name": "NAME_OF_THE_TOOL",
        "arguments": {
            "ARGUMENT_KEY": "ARGUMENT_VALUE"
        }
    }
}

If you have gathered enough information and are ready to fully answer the user's request, return this exact format:
{
    "thought": "I have all the necessary information from the files to answer.",
    "final_response": "Your complete, comprehensive, and detailed final answer to the user's prompt"
}

AVAILABLE TOOLS YOU CAN CALL:
1. get_files_info
   Arguments: {"directory": "."} or any relative subfolder.
2. get_file_content
   Arguments: {"file_path": "relative_path_to_file.py"}
3. write_file
   Arguments: {"file_path": "path.py", "content": "file_text_content"}
4. run_python_file
   Arguments: {"file_path": "path.py", "args": ["optional", "args"]}

Remember: NEVER guess. If you need to know how the calculator renders output, you MUST call get_files_info or get_file_content first!
"""

def extract_json(text: str) -> dict | None:
    """Próbuje wyczyścić tekst ze śmieci i wyciągnąć z niego czysty słownik JSON."""
    try:
        # Szukamy bloku między {}
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass
    return None

def main():
    warnings.filterwarnings("ignore")

    parser = argparse.ArgumentParser(description="Local AI Chatbot")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # POPRAWIONO: Nadano liście silny typ ChatCompletionMessageParam, co likwiduje błąd typowania
    messages: list[ChatCompletionMessageParam] = [
        {"role": "user", "content": f"{SYSTEM_PROMPT}\n\nUSER PROMPT: {args.user_prompt}"}
    ]
    
    console.print(Panel(f"[bold magenta]🚀 Local Prompt:[/bold magenta] {args.user_prompt}", title="[bold cyan]Ustrukturyzowany Lokalny Agent AI[/bold cyan]"))
    
    for i in range(20):
        with Live(Spinner("dots", text=f"[yellow] Local LLM is reasoning (Iteration {i + 1}/20)...[/yellow]"), refresh_per_second=15) as live:
            response = client.chat.completions.create(
                model="local-model",
                messages=messages,
                temperature=0.1  
            )
            
        ai_response_text = response.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": ai_response_text})
        
        # Próbujemy sparsować odpowiedź strukturalną
        data = extract_json(ai_response_text)
        
        if not data:
            console.print(f"[dim red]⚠️ Model produced unstructured response. Retrying with enforcement...[/dim red]")
            messages.append({"role": "user", "content": "ERROR: Your response was not a valid JSON. You MUST output ONLY the requested JSON structure."})
            continue

        if "thought" in data and args.verbose:
            console.print(f"[dim cyan]🧠 Thought:[/dim cyan] {data['thought']}")

        # OBSŁUGA WYWOŁANIA NARZĘDZIA
        if "tool_call" in data and data["tool_call"]:
            tool_data = data["tool_call"]
            function_name = tool_data.get("name", "")
            function_args_dict = tool_data.get("arguments", {})
            
            console.print(f"⚙️  [bold blue]Executing Tool:[/bold blue] [green]{function_name}[/green]")
            
            args_str = json.dumps(function_args_dict)
            if args.verbose:
                console.print(f"   [dim]Args: {args_str}[/dim]")
                
            tool_output = call_function_local(function_name, args_str, verbose=False)
            
            if args.verbose:
                console.print(f"   ↳ [italic green]Tool Output:[/italic green] [dim]{tool_output}[/dim]")
                
            messages.append({
                "role": "user",
                "content": json.dumps({"status": "success", "tool_result": tool_output})
            })
            continue

        # OBSŁUGA KOŃCOWEJ ODPOWIEDZI
        if "final_response" in data:
            console.print("\n")
            console.print(Panel(data["final_response"], title="[bold green]🎯 Final Response[/bold green]", border_style="green"))
            break
            
        messages.append({"role": "user", "content": "ERROR: Missing 'tool_call' or 'final_response' keys in your JSON."})

if __name__ == "__main__":
    main()
