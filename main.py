def add_book():
    pass


def remove_book():
    pass


def list_books():
    pass


def run_menu_option(menu_option):
    match menu_option:
        case 1:
            add_book()
        case 2:
            remove_book()
        case 3:
            list_books()
        case 4:
            print("Goodbye")
        case _:
            print("Unknown menu option, exiting.")


def select_menu_option():
    option_number = 0
    while True:
        if option_number > 0 and option_number < 5:
            break
        else:
            try:
                option_number = int(input("Select option: "))
            except:
                print("Input must be a valid number")
    run_menu_option(option_number)


def display_menu():
    print("\nPersonal Library Manager")
    print("1. Add book")
    print("2. Remove book")
    print("3. List books")
    print("4. Exit")
    select_menu_option()


def main():
    display_menu()


if __name__ == "__main__":
    main()