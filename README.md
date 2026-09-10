Author: Nate Downey 
Date: Sept 2026

Introduction

In this project, you will design and implement a command-line application called the Personal Library Manager. The goal of this project is to help you master Python’s built-in data structures and understand how design decisions evolve as a program grows in complexity. You will build a system that allows a user to store, search, update, analyze, and persist information about books in a personal library.

This project is intentionally structured to mirror real-world software development, where an initial simple solution is gradually refined into a more efficient and maintainable design. You are expected to think carefully about how data is stored, accessed, and modified throughout the program.

Project Objective

The objective of this project is to demonstrate your ability to select and use Python data structures appropriately. By the end of the project, your final implementation should clearly justify why dictionaries, lists, sets, and other structures were chosen, and how they improve efficiency, clarity, and extensibility.

Your solution must not simply work; it must be well-structured, readable, and thoughtfully designed.

Program Description

The Personal Library Manager is an interactive console program that allows users to manage a collection of books. Each book has a title, an author, and a year of publication. The user interacts with the program through a text-based menu and can perform operations such as adding new books, updating existing ones, removing books, searching by title, viewing the full collection, and generating summary statistics.

The program must also support saving the library data to a file and loading it again when the program starts. This ensures that the user’s data persists between program runs.

Final Data Model

In the final version of the project, the library must be stored as a dictionary where each key is a book title and each value is another dictionary containing the book’s attributes. This nested dictionary design allows for fast lookups by title and makes it easy to extend the program later by adding new attributes such as genre, rating, or reading status.

The title of a book must be unique within the library. If a user attempts to add a book with a title that already exists, the program should update the existing entry rather than create a duplicate.

Required Features

Your final program must allow the user to add a new book or update an existing book by entering its title, author, and year of publication. The user must be able to remove a book from the library by title. The program must display all stored books in a readable format, including an index number for each book to improve clarity for the user.

The program must support searching for books using partial title matches. Searches must be case-insensitive, and the program should clearly indicate when no matches are found.

In addition to basic CRUD operations, the program must generate statistics showing how many books each author has in the library. These statistics should be computed dynamically from the stored data rather than hard-coded or manually tracked.

Finally, the program must save all library data to a file before exiting and reload that data when it starts. If the data file does not exist, the program should start with an empty library without crashing.

Layered Development Strategy

You are expected to build this project in layers rather than jumping directly to the final design. In the first layer, you should use a simple list of strings to represent book titles. This version focuses on mastering loops, conditionals, and basic list operations.

In the second layer, you should enhance the data model by storing each book as a tuple containing the title, author, and year. At this stage, you should introduce a set to prevent duplicate titles and use sorting and comprehensions to analyze the data.

In the final layer, you should refactor the program to use a dictionary-based design. This change should significantly simplify searching, updating, and extending the program. You should clearly understand why this design is superior for the final version and be able to explain the trade-offs involved.

Design Considerations

You should pay careful attention to mutability and performance when choosing data structures. Lists and dictionaries are mutable and well-suited for collections that change over time. Dictionaries provide constant-time access by key, which makes them ideal for storing books indexed by title.

Readability is just as important as correctness. You should use descriptive variable names, write clear docstrings, and avoid overly complex one-line expressions when they reduce clarity. Comprehensions should be used where they make the code easier to understand, not harder.

Your program should be written in a way that makes future extensions easy. A well-designed final version should allow new book attributes or features to be added with minimal changes to existing code.

Input and Output Example

When the program starts, it should load any previously saved data and display the number of books currently in the library. The user should then be presented with a menu of options. When listing books, the program should display each book’s title, author, and publication year in a clean and readable format.

When a user searches for a book using a keyword, the program should display all matching titles along with their details. If no matches are found, the program should clearly state that no results were found.

When the user chooses to exit the program, the library data should be saved automatically, and the program should terminate gracefully.

Testing Expectations

Your project must be accompanied by a complete unit test file that tests both normal behavior and edge cases. This includes testing behavior when the library is empty, when duplicate titles are added, when searches return no results, and when files are missing.

Each test run must generate log files that record both the pass or fail status of each test and all console output produced during the test execution. This requirement reflects professional testing practices and emphasizes the importance of traceability and debugging.

Evaluation Criteria

Your project will be evaluated based on correctness, proper use of data structures, code readability, quality of documentation, and completeness of testing. You will also be assessed on your ability to explain your design decisions and demonstrate understanding of how the project evolved across layers.

Final Note

This project is not about writing the shortest solution possible. It is about writing a clear, correct, and well-reasoned solution that demonstrates your understanding of Python data structures and how they are used in real programs. Treat this project as a foundation you could realistically build upon in a larger application.

Deliverable

You must create a public GitHub repository and submit that link here. The project must be developed incrementally. Each new update should be pushed with a new commit. The commit messages should be detailed and explain the features implemented in that single commit. 