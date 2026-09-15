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


def exit_program():
    print("\nGoodbye")


def search_book():
    pass


def add_book():
    print("")
    while True:
        book_title = input("Enter book title to add (Blank line to exit): ")
        
        if (book_title == ""):
            break
        
        library.append(book_title)
        
    display_menu()


def remove_book():
    print("")
    while True:
        book_title = input("Enter book title to remove (Blank line to exit): ")
        
        if (book_title == ""):
            break
        elif (book_title in library):
            library.remove(book_title)
        else:
            print(f"{book_title} doesn't exist in library.")
        
    display_menu()


def list_books():
    if (len(library) > 0):
        print("\nLibrary:")
        for id, book in enumerate(library, start=1):
            print(f"{id}. {book}")
        display_menu()
    else:
        print("\nNo books in library.")
        display_menu()


def select_menu_option(options):
    option_number = 0
    while True:
        if 0 < option_number <= len(options):
            break
        else:
            try:
                option_number = int(input("Select option: "))
            except ValueError:
                print("Input must be a valid number.")
    options[option_number - 1]["function"]()


def display_menu():
    print("\nPersonal Library Manager")
    options = [
        {"text": "Add Book", "function": add_book},
        {"text": "Remove Book", "function": remove_book},
        {"text": "List Books", "function": list_books},
        {"text": "Search Book", "function": search_book},
        {"text": "Exit", "function": exit_program},
    ]
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option['text']}")
    select_menu_option(options)


def main():
    display_menu()


if __name__ == "__main__":
    main()