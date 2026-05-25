import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_targ_dic = os.path.commonpath([abs_path, target_path]) == abs_path
        if not valid_targ_dic:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dic = os.path.dirname(target_path)
        os.makedirs(parent_dic, exist_ok = True)

        with open(target_path, "w", encoding = "utf-8") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error {e}"



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites or creates a file with the specified content.",  # Usunięto tekst o .py
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the file to write to.",  # Usunięto tekst o .py
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

