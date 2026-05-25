import os
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.get_file_content import get_file_content

def main():
    print("=== ULTIMATE SECURITY SANDBOX TEST ===\n")
    
    # Atak 1: Próba przeczytania sekretów .env przez funkcję czytania plików (Path Traversal)
    print("Atak 1: Czytanie wrażliwego pliku systemowego przez relatywność:")
    print(get_file_content("calculator", "../.env"))
    print("-" * 50)
    
    # Atak 2: Próba wstrzyknięcia skryptu kradnącego tokeny przez zapis pliku (AST Block)
    malicious_script = """
import urllib.request
import os
# Próba wysłania tokenów na zewnątrz
token = os.environ.get('GEMINI_API_KEY')
print(f'Sending token... {token}')
"""
    print("Atak 2: Zapis złośliwego kodu (import os + sieciowe):")
    print(write_file("calculator", "pkg/exploit.py", malicious_script))
    print("-" * 50)
    
    # Atak 3: Próba uruchomienia zablokowanego skryptu (gdyby jakimś cudem przeszedł przez write)
    print("Atak 3: Próba wykonania kodu naruszającego AST Sandbox:")
    # Tworzymy tymczasowo plik z błędem bezpośrednio z poziomu testu, żeby sprawdzić silnik run_python_file
    os.makedirs("calculator/pkg", exist_ok=True)
    with open("calculator/pkg/fake_exploit.py", "w", encoding="utf-8") as f:
        f.write("import subprocess\nsubprocess.run(['ls', '/'])")
        
    print(run_python_file("calculator", "pkg/fake_exploit.py"))
    
    # Czyszczenie po teście 3
    if os.path.exists("calculator/pkg/fake_exploit.py"):
        os.remove("calculator/pkg/fake_exploit.py")

if __name__ == "__main__":
    main()
