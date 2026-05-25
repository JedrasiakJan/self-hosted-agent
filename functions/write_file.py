import os
from google.genai import types
from functions.security import is_code_safe  

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_targ_dic = os.path.commonpath([abs_path, target_path]) == abs_path
        
        if not valid_targ_dic:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            
        if not is_code_safe(content):
            return f'Error: Security Sandbox Blocked writing to "{file_path}". Code contains forbidden operations or imports.'
            
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dic = os.path.dirname(target_path)
        os.makedirs(parent_dic, exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f'Success: Successfully wrote to file "{file_path}"'
        
    except Exception as e:
        return f"Error: {str(e)}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites or creates a file with the specified content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the file to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
