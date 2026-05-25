from functions.write_file import write_file


def main():
    print("--- Test 1: Nadpisanie istniejącego pliku (lorem.txt) ---")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print()

    print("--- Test 2: Zapis w nowym podkatalogu (pkg/morelorem.txt) ---")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print()

    print("--- Test 3: Próba zapisu poza katalogiem roboczym (/tmp/temp.txt) ---")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    main()
