"""
Layer 1: Personal Library Manager - List of Titles
=====================================================
Purpose
-------
This is the FIRST layer of the Personal Library Manager project.
The goal here is not efficiency or good design -- it is to practice
basic Python control flow (loops, conditionals) and basic list
operations before introducing more advanced data structures.

Data Model
----------
The entire library is represented as a single list of strings:

    library = ["Dune", "1984", "The Hobbit"]

Limitations (intentional, to motivate Layer 2)
-----------------------------------------------
- Only the title is stored; there is no place for author or year.
- Checking for a duplicate title requires an O(n) linear scan.
- There is no structure for "author" statistics at all.

These limitations are exactly why the project moves on to Layer 2.
"""

library = []

def add_book():
    pass


def remove_book():
    pass


def list_books():
    if (len(library) > 0):
        for book in library:
            print(book)
        display_menu()
    else:
        print("\nNo books in library.")
        display_menu()


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