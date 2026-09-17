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