import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        valid_target_dir = os.path.commonpath([absolute_working_dir, target_file_path]) == absolute_working_dir
        
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
            
        with open(target_file_path, "r", encoding="utf-8") as f:
            file_contents = f.read(MAX_CHARS)
            if f.read(1):
                file_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_contents 
        
    except Exception as e:
        return f"Error: {str(e)}"
