from functions.get_file_content import get_file_content


def main():
    result_lorem = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt truncated: {'truncated' in result_lorem}")
    

    result_main = get_file_content("calculator", "main.py")
    print(result_main)
    

    result_calc = get_file_content("calculator", "pkg/calculator.py")
    print(result_calc)

    result_missing = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result_missing)


if __name__ == "__main__":
    main()
