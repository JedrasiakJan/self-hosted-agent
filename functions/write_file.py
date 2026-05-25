import os
from functions.security import is_code_safe  

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_targ_dic = os.path.commonpath([abs_path, target_path]) == abs_path
        
        # 1. Blokada Path Traversal
        if not valid_targ_dic:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            
        # 2. Blokada AST Sandbox
        if not is_code_safe(content):
            return f'Error: Security Sandbox Blocked writing to "{file_path}". Code contains forbidden operations or imports.'
            
        # 3. Blokada nadpisywania katalogów
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # 4. Automatyczne tworzenie struktury folderów nadrzędnych
        parent_dic = os.path.dirname(target_path)
        os.makedirs(parent_dic, exist_ok=True)

        # 5. Fizyczny zapis na dysku Windowsa
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f'Success: Successfully wrote to file "{file_path}"'
        
    except Exception as e:
        return f"Error: {str(e)}"
