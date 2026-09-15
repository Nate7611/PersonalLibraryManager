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


import os


library = []


# save file next to the script
LIBRARY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.txt")


def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                title = line.rstrip("\n")
                if title != "":
                    library.append(title)


def save_library():
    with open(LIBRARY_FILE, "w", encoding="utf-8") as f:
        for book in library:
            f.write(book + "\n")


def exit_program():
    save_library()
    print("\nGoodbye")


def matches_search(book, query):
    return query.lower() in book.lower()


def format_book(book):
    # Will format book dicts when implemented 
    return book


def search_book():
    print("")
    while True:
        query = input("Enter search term (Blank line to exit): ")
 
        if query == "":
            break
 
        results = [book for book in library if matches_search(book, query)]
 
        if results:
            print(f"\nFound {len(results)} matching book(s):")
            for id, book in enumerate(results, start=1):
                print(f"{id}. {format_book(book)}")
        else:
            print(f"\nNo results found for '{query}'.")
 
    display_menu()


def add_book():
    print("")
    while True:
        book_title = input("Enter book title to add (Blank line to exit): ")
        
        if (book_title == ""):
            break
        
        library.append(book_title)
        print(f"Added {book_title} to library.")
        
    save_library()
    display_menu()


def remove_book():
    print("")
    while True:
        book_title = input("Enter book title to remove (Blank line to exit): ")
        
        if (book_title == ""):
            break
        elif (book_title in library):
            library.remove(book_title)
            print(f"Removed {book_title} from library.")
        else:
            print(f"{book_title} doesn't exist in library.")
        
    save_library()
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
    load_library()
    display_menu()


if __name__ == "__main__":
    main()