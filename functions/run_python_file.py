import os
import subprocess
from functions.security import is_code_safe  

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
        validated_target = os.path.commonpath([abs_path, target_path]) == abs_path
        
        # 1. Zabezpieczenie ścieżki (Path Traversal)
        if not validated_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
        # 2. Sprawdzenie typu obiektu
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
            
        # 3. Weryfikacja rozszerzenia skryptu
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
            
        # 4. Odczyt zawartości pliku do analizy AST Sandbox
        with open(target_path, "r", encoding="utf-8") as f:
            code_to_run = f.read()
            
        # 5. Blokada bezpieczeństwa przed wykonaniem kodu
        if not is_code_safe(code_to_run):
            return f'Error: Security Sandbox Blocked execution of "{file_path}". File contains forbidden system commands.'

        # 6. Przygotowanie i uruchomienie podprocesu
        command = ["python", target_path]
        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=abs_path,
            stdout=subprocess.PIPE,       
            stderr=subprocess.PIPE,        
            text=True,                      
            timeout=30    
        )

        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")
                
        return "\n".join(output_parts)
        
    except Exception as e:
        return f"Error: {str(e)}"
