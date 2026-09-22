import json

import pytest
import main


@pytest.fixture(autouse=True)
def clean_library(tmp_path):
    main.library.clear()
    main.LIBRARY_FILE = tmp_path / "library.json"
    yield


def test_matches_search_is_case_insensitive():
    book = {"title": "Book", "author": "Author", "year": "2000"}
    assert main.matches_search(book, "book") is True


def test_matches_search_no_match():
    book = {"title": "Book", "author": "Author", "year": "2000"}
    assert main.matches_search(book, "xyz") is False


def test_format_book_formats_title_author_year():
    book = {"title": "A", "author": "B", "year": "2000"}
    assert main.format_book(book) == "A by B (2000)"


def test_save_library_writes_book_records():
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}
    main.library["b"] = {"title": "B", "author": "Y", "year": "2001"}

    main.save_library()

    saved = json.loads(main.LIBRARY_FILE.read_text(encoding="utf-8"))
    assert saved == [
        {"title": "A", "author": "X", "year": "2000"},
        {"title": "B", "author": "Y", "year": "2001"},
    ]


def test_load_library_reads_saved_books():
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}
    main.save_library()
    main.library.clear()

    main.load_library()

    assert main.library == {
        "a": {"title": "A", "author": "X", "year": "2000"}
    }


def test_load_library_reads_multiple_records():
    main.LIBRARY_FILE.write_text(
        json.dumps([
            {"title": "A", "author": "X", "year": "2000"},
            {"title": "B", "author": "Y", "year": "2001"},
        ]),
        encoding="utf-8",
    )

    main.load_library()

    assert main.library == {
        "a": {"title": "A", "author": "X", "year": "2000"},
        "b": {"title": "B", "author": "Y", "year": "2001"},
    }


def test_load_library_handles_invalid_json():
    main.LIBRARY_FILE.write_text("not valid json", encoding="utf-8")

    main.load_library()

    assert main.library == {}


def test_load_library_does_nothing_without_file():
    main.load_library()

    assert main.library == {}


def test_exit_program_saves_and_prints_goodbye(capsys):
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}

    main.exit_program()

    saved = json.loads(main.LIBRARY_FILE.read_text(encoding="utf-8"))
    assert saved == [{"title": "A", "author": "X", "year": "2000"}]
    assert "Goodbye" in capsys.readouterr().out


def test_add_book_adds_titles_and_saves(monkeypatch):
    answers = iter([
        "A", "X", "2000",
        "B", "Y", "2001",
        "",
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.add_book()

    assert main.library == {
        "a": {"title": "A", "author": "X", "year": "2000"},
        "b": {"title": "B", "author": "Y", "year": "2001"},
    }
    saved = json.loads(main.LIBRARY_FILE.read_text(encoding="utf-8"))
    assert saved == [
        {"title": "A", "author": "X", "year": "2000"},
        {"title": "B", "author": "Y", "year": "2001"},
    ]


def test_add_book_strips_whitespace(monkeypatch):
    answers = iter(["  A  ", "  X  ", "  2000  ", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.add_book()

    assert main.library == {"a": {"title": "A", "author": "X", "year": "2000"}}


def test_add_book_updates_existing_title_case_insensitively(monkeypatch, capsys):
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}
    answers = iter(["a", "Y", "2001", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.add_book()

    assert main.library == {
        "a": {"title": "a", "author": "Y", "year": "2001"}
    }
    assert "Updated a in library" in capsys.readouterr().out


def test_add_book_updating_does_not_create_duplicate_entry(monkeypatch):
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}
    answers = iter(["A", "X", "2000", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.add_book()

    assert len(main.library) == 1
    assert main.library == {"a": {"title": "A", "author": "X", "year": "2000"}}


def test_remove_book_removes_existing_title(monkeypatch):
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}
    main.library["b"] = {"title": "B", "author": "Y", "year": "2001"}
    answers = iter(["A", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.remove_book()

    assert main.library == {"b": {"title": "B", "author": "Y", "year": "2001"}}


def test_remove_book_matches_case_insensitively(monkeypatch):
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}
    answers = iter(["a", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.remove_book()

    assert main.library == {}


def test_remove_book_keeps_missing_title_and_prints_message(monkeypatch, capsys):
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}
    answers = iter(["B", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.remove_book()

    assert main.library == {"a": {"title": "A", "author": "X", "year": "2000"}}
    assert "doesn't exist in library" in capsys.readouterr().out


def test_list_books_prints_numbered_books(monkeypatch, capsys):
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}
    main.library["b"] = {"title": "B", "author": "Y", "year": "2001"}
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.list_books()

    out = capsys.readouterr().out
    assert "1. A by X (2000)" in out
    assert "2. B by Y (2001)" in out


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
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}
    main.library["b"] = {"title": "B", "author": "Y", "year": "2001"}
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.print_author_stats()

    out = capsys.readouterr().out
    assert "Books per author:" in out
    assert "X: 1" in out
    assert "Y: 1" in out


def test_print_author_stats_counts_multiple_books_by_same_author(monkeypatch, capsys):
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}
    main.library["b"] = {"title": "B", "author": "X", "year": "2000"}
    main.library["c"] = {"title": "C", "author": "X", "year": "2000"}
    main.library["d"] = {"title": "D", "author": "Y", "year": "2001"}
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.print_author_stats()

    out = capsys.readouterr().out
    assert "X: 3" in out
    assert "Y: 1" in out


def test_print_author_stats_empty_library_prints_message(monkeypatch, capsys):
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.print_author_stats()

    out = capsys.readouterr().out
    assert "No books in library." in out
    assert "Books per author:" not in out


def test_print_author_stats_returns_to_menu(monkeypatch):
    called = []
    main.library["a"] = {"title": "A", "author": "X", "year": "2000"}
    monkeypatch.setattr(main, "display_menu", lambda: called.append(True))

    main.print_author_stats()

    assert called == [True]