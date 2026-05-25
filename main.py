import argparse
import os
import sys
import warnings
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("Where is the API KEY?")

client = genai.Client(api_key=api_key)


def main():
    warnings.filterwarnings("ignore", message=".*non-text parts.*")

    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    
    for i in range(20):
        if args.verbose:
            print(f"\n--- Iteration {i + 1} ---")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, 
                temperature=0,
                tools=[available_functions]
            ),
        )
        
        if response.usage_metadata is None:
            raise RuntimeError("API request failed: usage_metadata is missing.")
            
        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # 1. Zapisujemy odpowiedź modelu dbając o poprawną strukturę i rolę
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    # Gwarantujemy, że rola to "model", jeśli biblioteka jej nie ustawiła
                    content_to_append = candidate.content
                    if not content_to_append.role:
                        content_to_append.role = "model"
                    messages.append(content_to_append)

        # 2. Wykonujemy funkcje i zbieramy ich części (parts)
        function_responses = []
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                
                if not function_call_result.parts:
                    raise RuntimeError("Validation failed: .parts list is empty.")
                    
                first_part = function_call_result.parts[0]
                
                if first_part.function_response is None:
                    raise RuntimeError("Validation failed: .function_response is None.")
                    
                if first_part.function_response.response is None:
                    raise RuntimeError("Validation failed: .response field is None.")
                
                function_responses.append(first_part)

        # 3. Jeśli wywołano funkcje, przekazujemy je do historii i kontynuujemy pętlę
        if function_responses:
            messages.append(types.Content(role="user", parts=function_responses))
            continue

        # 4. Zakończenie sukcesem
        if response.text:
            print("Final response:")
            print(response.text)
            break
    else:
        print("Error: Agent reached the maximum number of iterations without a final response.")
        sys.exit(1)


if __name__ == "__main__":
    main()
