import pytest
import main


@pytest.fixture(autouse=True)
def clean_library(tmp_path):
    main.library.clear()
    main.LIBRARY_FILE = tmp_path / "library.txt"
    yield


def test_matches_search_is_case_insensitive():
    assert main.matches_search("The Hobbit", "hobbit") is True


def test_matches_search_no_match():
    assert main.matches_search("The Hobbit", "dune") is False


def test_format_book_returns_book():
    assert main.format_book("Dune") == "Dune"


def test_save_library_writes_one_title_per_line():
    main.library.extend(["Dune", "The Hobbit"])

    main.save_library()

    content = main.LIBRARY_FILE.read_text(encoding="utf-8")
    assert content == "Dune\nThe Hobbit\n"


def test_load_library_reads_saved_books():
    main.library.extend(["Dune"])
    main.save_library()
    main.library.clear()

    main.load_library()

    assert main.library == ["Dune"]


def test_load_library_skips_blank_lines():
    main.LIBRARY_FILE.write_text("Dune\n\nThe Hobbit\n", encoding="utf-8")

    main.load_library()

    assert main.library == ["Dune", "The Hobbit"]


def test_load_library_does_nothing_without_file():
    main.load_library()

    assert main.library == []


def test_exit_program_saves_and_prints_goodbye(capsys):
    main.library.append("Dune")

    main.exit_program()

    assert main.LIBRARY_FILE.read_text(encoding="utf-8") == "Dune\n"
    assert "Goodbye" in capsys.readouterr().out
 

def test_add_book_adds_titles_and_saves(monkeypatch):
    answers = iter(["Dune", "The Hobbit", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.add_book()

    assert main.library == ["Dune", "The Hobbit"]
    assert main.LIBRARY_FILE.read_text(encoding="utf-8") == "Dune\nThe Hobbit\n"


def test_add_book_strips_whitespace(monkeypatch):
    answers = iter(["  Dune  ", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.add_book()

    assert main.library == ["Dune"]


def test_remove_book_removes_existing_title(monkeypatch):
    main.library.extend(["Dune", "The Hobbit"])
    answers = iter(["Dune", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.remove_book()

    assert main.library == ["The Hobbit"]


def test_remove_book_keeps_missing_title_and_prints_message(monkeypatch, capsys):
    main.library.append("Dune")
    answers = iter(["Hobbit", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(main, "display_menu", lambda: None)

    main.remove_book()

    assert main.library == ["Dune"]
    assert "doesn't exist in library" in capsys.readouterr().out