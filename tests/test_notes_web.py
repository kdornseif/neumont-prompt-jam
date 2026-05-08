"""
tests/test_notes_web.py

Tests for Flask web interactions.

Version: 0.2.0

Testing guideline used:
Arrange / Act / Assert.

These tests use Flask's built-in test client. They verify browser-like
interactions without launching a real browser.
"""

import notes_web
from notes_core import NoteStore


def create_test_client():
    """
    Create a Flask test client with a fresh NoteStore.

    The web app uses a module-level store for beginner simplicity.
    Tests reset that store before each test to avoid test pollution.
    """
    notes_web.app.config.update(TESTING=True)
    notes_web.store = NoteStore()
    return notes_web.app.test_client()


def test_web_index_shows_starter_notes():
    """
    Verify that the home page displays starter notes.

    Arrange: Create a test client.
    Act: Request the home page.
    Assert: The response should include starter note text.
    """
    client = create_test_client()

    response = client.get("/")

    page_text = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Personal Notes App v0.2.0" in page_text
    assert "Review Python functions" in page_text


def test_web_add_note_adds_note_and_redirects():
    """
    Verify that the web app can add a note.

    Arrange: Create a test client.
    Act: POST a note to the add route.
    Assert: The redirected page should show the new note.
    """
    client = create_test_client()

    response = client.post(
        "/add",
        data={"note_text": "Web note"},
        follow_redirects=True
    )

    page_text = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Note added." in page_text
    assert "Web note" in page_text


def test_web_add_blank_note_shows_error():
    """
    Verify that the web app displays an error for blank notes.

    Arrange: Create a test client.
    Act: POST a blank note.
    Assert: The page should show the validation error.
    """
    client = create_test_client()

    response = client.post(
        "/add",
        data={"note_text": "   "},
        follow_redirects=True
    )

    page_text = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Error: Note text cannot be empty." in page_text


def test_web_remove_note_removes_note():
    """
    Verify that the web app can remove a note.

    Arrange: Create a test client.
    Act: POST note ID 1 to the remove route.
    Assert: The removed note should no longer appear.
    """
    client = create_test_client()

    response = client.post(
        "/remove",
        data={"note_id": "1"},
        follow_redirects=True
    )

    page_text = response.data.decode("utf-8")

    assert response.status_code == 200
    assert 'Removed note: "Review Python functions"' in page_text
    assert "1. Review Python functions" not in page_text


def test_web_remove_missing_note_shows_error():
    """
    Verify that removing a missing note ID shows an error.

    Arrange: Create a test client.
    Act: POST a missing note ID.
    Assert: The page should show an error.
    """
    client = create_test_client()

    response = client.post(
        "/remove",
        data={"note_id": "999"},
        follow_redirects=True
    )

    page_text = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Error: No note found with ID 999." in page_text


def test_web_save_without_source_shows_error():
    """
    Verify that web save handles missing source/target.

    Arrange: Create a test client without loading or saving as CSV.
    Act: POST to save.
    Assert: The page should show a clear error.
    """
    client = create_test_client()

    response = client.post("/save", follow_redirects=True)

    page_text = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Error saving notes:" in page_text


def test_web_save_as_csv_creates_file(tmp_path):
    """
    Verify that web save-as creates a CSV file.

    Arrange: Create a test client and temporary CSV path.
    Act: POST to save-as CSV.
    Assert: The file should exist and page should show confirmation.
    """
    client = create_test_client()
    csv_path = tmp_path / "web_notes.csv"

    response = client.post(
        "/save-as-csv",
        data={"file_path": str(csv_path)},
        follow_redirects=True
    )

    page_text = response.data.decode("utf-8")

    assert response.status_code == 200
    assert csv_path.exists()
    assert "Notes saved as CSV." in page_text


def test_web_load_csv_loads_notes(tmp_path):
    """
    Verify that web load CSV replaces notes.

    Arrange: Create a CSV file and a test client.
    Act: POST the file path to load CSV.
    Assert: The page should show imported notes.
    """
    client = create_test_client()
    csv_path = tmp_path / "web_load.csv"

    csv_path.write_text("id,text\n7,Loaded through web\n", encoding="utf-8")

    response = client.post(
        "/load-csv",
        data={"file_path": str(csv_path)},
        follow_redirects=True
    )

    page_text = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Notes loaded from CSV." in page_text
    assert "Loaded through web" in page_text