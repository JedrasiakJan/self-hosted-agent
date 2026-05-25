from collections.abc import Callable
from google.genai import types

# Import rzeczywistych funkcji wykonawczych i ich schematów
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

# Lista wszystkich narzędzi dostępnych dla modelu Gemini
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ],
)

# Definicja mapowania nazw na obiekty wywoływalne (zgodnie z instrukcją)
function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(
    function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:
    # Bezpieczne pobranie nazwy jako ciąg tekstowy
    function_name = function_call.name or ""

    # Formatowanie wypisywania informacji w konsoli na podstawie flagi verbose
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    # Sprawdzenie, czy funkcja znajduje się w słowniku mapowania
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Tworzenie płytkiej kopii argumentów (lub pustego słownika, jeśli args to None)
    args = dict(function_call.args) if function_call.args else {}
    
    # Nadpisanie/ustawienie katalogu roboczego zgodnie z wymaganiem ("./calculator")
    args["working_directory"] = "./calculator"

    # Wywołanie właściwej funkcji z przekazaniem argumentów słownikowych
    function_result = function_map[function_name](**args)

    # Zwrócenie wyniku opakowanego przy użyciu from_function_response
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
