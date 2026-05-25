import ast

def is_code_safe(code_string: str) -> bool:
    """
    Analizuje kod za pomocą Abstract Syntax Tree (AST).
    Blokuje niebezpieczne importy oraz funkcje przed wykonaniem przez LLM.
    """
    # Czarne listy elementów niedozwolonych dla agenta AI
    forbidden_modules = {"os", "subprocess", "shutil", "sys", "builtins", "requests"}
    forbidden_functions = {"eval", "exec", "open", "compile", "globals", "locals"}
    
    try:
        # Parsowanie surowego stringa tekstowego do drzewa składniowego
        tree = ast.parse(code_string)
        
        # Iteracja po każdym elemencie (węźle) w drzewie kodu
        for node in ast.walk(tree):
            # 1. Wykrywanie tradycyjnych importów (np. import os, import subprocess)
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in forbidden_modules or alias.name.split('.')[0] in forbidden_modules:
                        return False
                        
            # 2. Wykrywanie importów selektywnych (np. from os import system)
            elif isinstance(node, ast.ImportFrom):
                if node.module and (node.module in forbidden_modules or node.module.split('.')[0] in forbidden_modules):
                    return False
                    
            # 3. Wykrywanie bezpośrednich wywołań zakazanych funkcji (np. eval("...") lub open())
            elif isinstance(node, ast.Call):
                # Obsługa prostych wywołań: funkcja()
                if isinstance(node.func, ast.Name):
                    if node.func.id in forbidden_functions:
                        return False
                # Obsługa wywołań obiektowych: moduł.funkcja() (np. os.system())
                elif isinstance(node.func, ast.Attribute):
                    if node.func.attr in forbidden_functions:
                        return False
                        
        return True
    except Exception:
        # Jeśli kod ma błędy składniowe i nie da się go sparsować, traktujemy go jako niebezpieczny
        return False
