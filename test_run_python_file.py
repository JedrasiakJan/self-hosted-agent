from functions.run_python_file import run_python_file


def main():
    print("--- Test 1: Uruchomienie main.py bez argumentów (instrukcja użycia) ---")
    print(run_python_file("calculator", "main.py"))
    print("\n" + "="*50 + "\n")

    print("--- Test 2: Uruchomienie kalkulatora z działaniem '3 + 5' ---")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("\n" + "="*50 + "\n")

    print("--- Test 3: Uruchomienie testów kalkulatora (tests.py) ---")
    print(run_python_file("calculator", "tests.py"))
    print("\n" + "="*50 + "\n")

    print("--- Test 4: Próba wyjścia poza katalog roboczy (../main.py) ---")
    print(run_python_file("calculator", "../main.py"))
    print("\n" + "="*50 + "\n")

    print("--- Test 5: Próba uruchomienia nieistniejącego pliku (nonexistent.py) ---")
    print(run_python_file("calculator", "nonexistent.py"))
    print("\n" + "="*50 + "\n")

    print("--- Test 6: Próba uruchomienia pliku tekstowego (lorem.txt) ---")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()
