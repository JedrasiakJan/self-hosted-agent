import os
from collections.abc import Callable

# Import rzeczywistych funkcji wykonawczych
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Słownik mapujący nazwy na funkcje (zostaje bez zmian)
function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

# --- NOWA LISTA NARZĘDZI W STANDARDZIE OPENAI / LM STUDIO ---
available_functions = [
    {
        "type": "function",
        "function": {
            "name": "get_files_info",
            "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path to list files from, relative to the working directory.",
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_file_content",
            "description": "Reads and returns the contents of a specific file. Paths must be relative to the working directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The relative path of the file to read.",
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Overwrites or creates a file with the specified content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The relative path of the file to write to.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The text content to write into the file.",
                    }
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_python_file",
            "description": "Executes a specified Python file within the working directory using a subprocess and returns its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The relative path of the Python file to execute.",
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of command-line arguments to pass to the script.",
                    }
                },
                "required": ["file_path"]
            }
        }
    }
]

import json

def call_function_local(name: str, args_json_str: str, verbose: bool = False) -> str:
    """Wywołuje lokalną funkcję na podstawie danych z LM Studio i zwraca czysty tekst."""
    if verbose:
        print(f"Calling function: {name}({args_json_str})")
    else:
        print(f" - Calling function: {name}")

    if name not in function_map:
        return f"Error: Unknown function: {name}"

    try:
        # Dekodujemy argumenty przesłane jako JSON string przez LM Studio
        args = json.loads(args_json_str) if args_json_str else {}
    except Exception:
        args = {}

    # Zabezpieczenie katalogu roboczego
    args["working_directory"] = "./calculator"

    # Wywołanie funkcji
    try:
        return function_map[name](**args)
    except Exception as e:
        return f"Error: {str(e)}"
