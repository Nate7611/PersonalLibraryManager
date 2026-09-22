import json

import pytest
import main


@pytest.fixture(autouse=True)
def clean_library(tmp_path):
    main.library.clear()
    main.book_titles.clear()
    main.LIBRARY_FILE = tmp_path / "library.json"
    yield


def test_matches_search_is_case_insensitive():
    book = ("The Hobbit", "J.R.R. Tolkien", "1937")
    assert main.matches_search(book, "hobbit") is True


def test_matches_search_no_match():
    book = ("The Hobbit", "J.R.R. Tolkien", "1937")
    assert main.matches_search(book, "dune") is False


def test_format_book_formats_title_author_year():
    book = ("Dune", "Frank Herbert", "1965")
    assert main.format_book(book) == "Dune by Frank Herbert (1965)"


def test_find_book_by_title_matches_case_insensitively():
    main.library.append(("Dune", "Frank Herbert", "1965"))

    found = main.find_book_by_title("dune")

    assert found == ("Dune", "Frank Herbert", "1965")


def test_find_book_by_title_returns_none_when_missing():
    assert main.find_book_by_title("Dune") is None


def test_save_library_writes_book_records():
    main.library.extend([
        ("Dune", "Frank Herbert", "1965"),
        ("The Hobbit", "J.R.R. Tolkien", "1937"),
    ])

    main.save_library()

    saved = json.loads(main.LIBRARY_FILE.read_text(encoding="utf-8"))
    assert saved == [
        {"title": "Dune", "author": "Frank Herbert", "year": "1965"},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": "1937"},
    ]


def test_load_library_reads_saved_books():
    main.library.extend([("Dune", "Frank Herbert", "1965")])
    main.save_library()
    main.library.clear()
    main.book_titles.clear()

    main.load_library()

    assert main.library == [("Dune", "Frank Herbert", "1965")]
    assert main.book_titles == {"dune"}


def test_load_library_reads_multiple_records():
    main.LIBRARY_FILE.write_text(
        json.dumps([
            {"title": "Dune", "author": "Frank Herbert", "year": "1965"},
            {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": "1937"},
        ]),
        encoding="utf-8",
    )

    main.load_library()

    assert main.library == [
        ("Dune", "Frank Herbert", "1965"),
        ("The Hobbit", "J.R.R. Tolkien", "1937"),
    ]


def test_load_library_handles_invalid_json():
    main.LIBRARY_FILE.write_text("not valid json", encoding="utf-8")

    main.load_library()

    assert main.library == []


def test_load_library_does_nothing_without_file():
    main.load_library()

    assert main.library == []


def test_exit_program_saves_and_prints_goodbye(capsys):
    main.library.append(("Dune", "Frank Herbert", "1965"))

    main.exit_program()

    saved = json.loads(main.LIBRARY_FILE.read_text(encoding="utf-8"))
    assert saved == [{"title": "Dune", "author": "Frank Herbert", "year": "1965"}]
    assert "Goodbye" in capsys.readouterr().out


def test_add_book_adds_titles_and_saves(monkeypatch):
    answers = iter([
        "Dune", "Frank Herbert", "1965",
        "The Hobbit", "J.R.R. Tolkien", "1937",
        "",
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.add_book()

    assert main.library == [
        ("Dune", "Frank Herbert", "1965"),
        ("The Hobbit", "J.R.R. Tolkien", "1937"),
    ]
    saved = json.loads(main.LIBRARY_FILE.read_text(encoding="utf-8"))
    assert saved == [
        {"title": "Dune", "author": "Frank Herbert", "year": "1965"},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": "1937"},
    ]


def test_add_book_strips_whitespace(monkeypatch):
    answers = iter(["  Dune  ", "  Frank Herbert  ", "  1965  ", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.add_book()

    assert main.library == [("Dune", "Frank Herbert", "1965")]


def test_add_book_rejects_duplicate_titles_case_insensitively(monkeypatch, capsys):
    main.library.append(("Dune", "Frank Herbert", "1965"))
    main.book_titles.add("dune")
    answers = iter(["dune", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.add_book()

    assert main.library == [("Dune", "Frank Herbert", "1965")]
    assert "already exists in library" in capsys.readouterr().out


def test_remove_book_removes_existing_title(monkeypatch):
    main.library.extend([
        ("Dune", "Frank Herbert", "1965"),
        ("The Hobbit", "J.R.R. Tolkien", "1937"),
    ])
    main.book_titles.update({"dune", "the hobbit"})
    answers = iter(["Dune", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.remove_book()

    assert main.library == [("The Hobbit", "J.R.R. Tolkien", "1937")]
    assert "dune" not in main.book_titles


def test_remove_book_matches_case_insensitively(monkeypatch):
    main.library.append(("The Hobbit", "J.R.R. Tolkien", "1937"))
    main.book_titles.add("the hobbit")
    answers = iter(["the hobbit", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.remove_book()

    assert main.library == []
    assert "the hobbit" not in main.book_titles


def test_remove_book_keeps_missing_title_and_prints_message(monkeypatch, capsys):
    main.library.append(("Dune", "Frank Herbert", "1965"))
    answers = iter(["Hobbit", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.remove_book()

    assert main.library == [("Dune", "Frank Herbert", "1965")]
    assert "doesn't exist in library" in capsys.readouterr().out


def test_list_books_prints_numbered_books(monkeypatch, capsys):
    main.library.extend([
        ("Dune", "Frank Herbert", "1965"),
        ("The Hobbit", "J.R.R. Tolkien", "1937"),
    ])
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.list_books()

    out = capsys.readouterr().out
    assert "1. Dune by Frank Herbert (1965)" in out
    assert "2. The Hobbit by J.R.R. Tolkien (1937)" in out


def test_select_menu_option_runs_chosen_function(monkeypatch):
    called = []
    options = [
        {"text": "A", "function": lambda: called.append("A")},
        {"text": "B", "function": lambda: called.append("B")},
    ]
    monkeypatch.setattr("builtins.input", lambda _: "2")

    main.select_menu_option(options)

    assert called == ["B"]


def test_select_menu_option_repeats_on_bad_input(monkeypatch):
    called = []
    options = [{"text": "A", "function": lambda: called.append("A")}]
    answers = iter(["not a number", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    main.select_menu_option(options)

    assert called == ["A"]


def test_print_author_stats_counts_single_book_per_author(monkeypatch, capsys):
    main.library.extend([
        ("Dune", "Frank", "1999"),
        ("The Hobbit", "Tolkien", "1999"),
    ])
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.print_author_stats()

    out = capsys.readouterr().out
    assert "Books per author:" in out
    assert "Frank: 1" in out
    assert "Tolkien: 1" in out


def test_print_author_stats_counts_multiple_books_by_same_author(monkeypatch, capsys):
    main.library.extend([
        ("Dune", "Frank", "1999"),
        ("Dune 2", "Frank", "1999"),
        ("Dune 3", "Frank", "1999"),
        ("The Hobbit", "Tolkien", "1999"),
    ])
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.print_author_stats()

    out = capsys.readouterr().out
    assert "Frank: 3" in out
    assert "Tolkien: 1" in out


def test_print_author_stats_empty_library_prints_message(monkeypatch, capsys):
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.print_author_stats()

    out = capsys.readouterr().out
    assert "No books in library." in out
    assert "Books per author:" not in out


def test_print_author_stats_returns_to_menu(monkeypatch):
    called = []
    main.library.append(("Dune", "Frank", "1999"))
    monkeypatch.setattr(main, "display_menu", lambda: called.append(True))

    main.print_author_stats()

    assert called == [True]