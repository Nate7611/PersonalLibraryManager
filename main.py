import json
import os

library = {}

# save file next to the script
LIBRARY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.json")


def load_library():
    """
    Load books from LIBRARY_FILE into the library dict, keyed by lowercased title.
    Does nothing if the file is missing; treats invalid JSON as no records.

    Params: none.
    Returns: None.
    """
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
            try:
                records = json.load(f)
            except json.JSONDecodeError:
                records = []

        for record in records:
            title = record.get("title", "")
            author = record.get("author", "Unknown")
            year = record.get("year", "Unknown")
            library[title.lower()] = {"title": title, "author": author, "year": year}

        print(f"Loaded {len(records)} books from {os.path.basename(LIBRARY_FILE)}.")


def save_library():
    """
    Write the library dict to LIBRARY_FILE as a JSON array of book records.

    Params: none.
    Returns: None.
    """
    records = list(library.values())
    with open(LIBRARY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def exit_program():
    """
    Save the library to disk and print a goodbye message before quitting.

    Params: none.
    Returns: None.
    """
    save_library()
    print(f"\nLibrary saved to {os.path.basename(LIBRARY_FILE)}. Goodbye!")


def print_author_stats():
    """
    Print how many books each author has in the library.

    Params: none.
    Returns: None. Returns control to the menu when done.
    """
    if len(library) > 0:
        counts = {}
        for book in library.values():
            counts[book["author"]] = counts.get(book["author"], 0) + 1

        print("\nBooks per author:")
        for author, count in counts.items():
            print(f"{author}: {count}")
    else:
        print("\nNo books in library.")

    display_menu()


def matches_search(book, query):
    """
    Check whether a search query appears in a book's title, case-insensitively.

    Params:
        book (dict): A {"title", "author", "year"} book record.
        query (str): The search term to look for.
    Returns:
        bool: True if query is found in the book's title, False otherwise.
    """
    return query.lower() in book["title"].lower()


def format_book(book):
    """
    Format a book entry for display.

    Params:
        book (dict): A {"title", "author", "year"} book record.
    Returns:
        str: A human-readable "Title by Author (Year)" string.
    """
    return f"{book['title']} by {book['author']} ({book['year']})"


def search_book():
    """
    Repeatedly prompt for a search term and print matching books until blank input.

    Params: none.
    Returns: None. Returns control to the menu when done.
    """
    print("")
    while True:
        query = input("Enter search term (Blank line to exit): ")

        if query == "":
            break

        results = [book for book in library.values() if matches_search(book, query)]

        if results:
            print(f"\nFound {len(results)} matching book(s):")
            for id, book in enumerate(results, start=1):
                print(f"{id}. {format_book(book)}")
        else:
            print(f"\nNo results found for '{query}'.")

    display_menu()


def add_book():
    """
    Repeatedly prompt for a book's title, author, and year and add each as
    a record to the library until a blank title is entered. If the title
    already exists in the library (case-insensitive), its author and year
    are overwritten in place instead of adding a duplicate entry.

    Params: none.
    Returns: None. Saves the library and returns control to the menu when done.
    """
    print("")
    while True:
        book_title = input("Enter book title to add (Blank line to exit): ").strip()

        if book_title == "":
            break

        author = input("Enter author: ").strip()
        while author == "":
            author = input("Author cannot be blank. Enter author: ").strip()
            
        year = input("Enter year published (blank if unknown): ").strip()
        while year != "" and not year.isdigit():
            year = input("Year must be a number, or blank if unknown: ").strip()
        if year == "":
            year = None

        key = book_title.lower()
        is_update = key in library
        library[key] = {"title": book_title, "author": author, "year": year}

        if is_update:
            print(f"Updated {book_title} in library.\n")
        else:
            print(f"Added {book_title} to library.\n")

    save_library()
    display_menu()


def remove_book():
    """
    Repeatedly prompt for book titles and remove each matching book from
    the library until blank input.

    Params: none.
    Returns: None. Saves the library and returns control to the menu when done.
    """
    print("")
    while True:
        book_title = input("Enter book title to remove (Blank line to exit): ").strip()

        if book_title == "":
            break

        key = book_title.lower()
        book = library.get(key)

        if book is not None:
            del library[key]
            print(f"Removed {book['title']} from library.\n")
        else:
            print(f"{book_title} doesn't exist in library.")

    save_library()
    display_menu()


def list_books():
    """
    Print every book currently in the library, numbered, or a message if empty.

    Params: none.
    Returns: None. Returns control to the menu when done.
    """
    if len(library) > 0:
        print("\nLibrary:")
        for id, book in enumerate(library.values(), start=1):
            print(f"{id}. {format_book(book)}")
        display_menu()
    else:
        print("\nNo books in library.")
        display_menu()


def select_menu_option(options):
    """
    Prompt the user for a menu number and call the matching option's function.

    Params:
        options (list[dict]): Menu options, each with a "text" label and a "function" callback.
    Returns: None.
    """
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
    """
    Print the main menu and hand off to select_menu_option to run the chosen action.

    Params: none.
    Returns: None.
    """
    print("\nPersonal Library Manager")
    options = [
        {"text": "Add or Update Book", "function": add_book},
        {"text": "Remove Book", "function": remove_book},
        {"text": "List Books", "function": list_books},
        {"text": "Search Book", "function": search_book},
        {"text": "Show Author Statistics", "function": print_author_stats},
        {"text": "Exit", "function": exit_program},
    ]
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option['text']}")
    select_menu_option(options)


def main():
    """
    Load the saved library and start the interactive menu loop.

    Params: none.
    Returns: None.
    """
    load_library()
    display_menu()


if __name__ == "__main__":
    main()