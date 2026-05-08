"""
tests/test_notes_cli.py

Tests for CLI interaction functions.

Version: 0.2.0

Testing guideline used:
Arrange / Act / Assert.

These tests intentionally focus on small CLI functions instead of trying to
automate a long terminal session. That keeps the tests simple and maintainable.
"""

from notes_cli import add_note, list_notes, load_from_csv, remove_note, save, save_as_csv
from notes_core import NoteStore


def test_cli_list_notes_prints_existing_notes(capsys):
    """
    Verify that the CLI can list notes.

    Arrange: Create a NoteStore.
    Act: Call list_notes.
    Assert: The printed output should include starter notes.
    """
    store = NoteStore()

    list_notes(store)

    captured = capsys.readouterr()

    assert "Your notes:" in captured.out
    assert "1. Review Python functions" in captured.out


def test_cli_add_note_reads_input_and_adds_note(monkeypatch, capsys):
    """
    Verify that the CLI can add a note using terminal input.

    Arrange: Mock input to return a note.
    Act: Call add_note.
    Assert: The note should be added and confirmation should be printed.
    """
    store = NoteStore()

    monkeypatch.setattr("builtins.input", lambda prompt: "CLI note")

    add_note(store)

    captured = capsys.readouterr()

    assert store.list_notes()[-1] == {"id": 4, "text": "CLI note"}
    assert "Note added." in captured.out


def test_cli_add_blank_note_prints_error(monkeypatch, capsys):
    """
    Verify that the CLI handles blank note input.

    Arrange: Mock input to return a blank note.
    Act: Call add_note.
    Assert: The CLI should print a clear error.
    """
    store = NoteStore()

    monkeypatch.setattr("builtins.input", lambda prompt: "   ")

    add_note(store)

    captured = capsys.readouterr()

    assert "Error: Note text cannot be empty." in captured.out


def test_cli_remove_note_reads_id_and_removes_note(monkeypatch, capsys):
    """
    Verify that the CLI can remove a note by ID.

    Arrange: Mock input to return note ID 1.
    Act: Call remove_note.
    Assert: Note 1 should be removed.
    """
    store = NoteStore()

    monkeypatch.setattr("builtins.input", lambda prompt: "1")

    remove_note(store)

    captured = capsys.readouterr()

    remaining_ids = [note["id"] for note in store.list_notes()]

    assert 1 not in remaining_ids
    assert 'Removed note: "Review Python functions"' in captured.out


def test_cli_remove_note_with_invalid_input_prints_error(monkeypatch, capsys):
    """
    Verify that the CLI handles non-numeric remove input.

    Arrange: Mock input to return text instead of a number.
    Act: Call remove_note.
    Assert: The CLI should print a validation message.
    """
    store = NoteStore()

    monkeypatch.setattr("builtins.input", lambda prompt: "abc")

    remove_note(store)

    captured = capsys.readouterr()

    assert "Please enter a valid numeric note ID." in captured.out


def test_cli_save_as_csv_creates_file(monkeypatch, capsys, tmp_path):
    """
    Verify that CLI save-as writes a CSV file.

    Arrange: Mock input to return a temporary CSV path.
    Act: Call save_as_csv.
    Assert: The file should exist and confirmation should be printed.
    """
    store = NoteStore()
    csv_path = tmp_path / "cli_notes.csv"

    monkeypatch.setattr("builtins.input", lambda prompt: str(csv_path))

    save_as_csv(store)

    captured = capsys.readouterr()

    assert csv_path.exists()
    assert "Notes saved as CSV." in captured.out


def test_cli_load_from_csv_loads_file(monkeypatch, capsys, tmp_path):
    """
    Verify that CLI load reads a CSV file path and loads notes.

    Arrange: Create a CSV file and mock input to return its path.
    Act: Call load_from_csv.
    Assert: The store should contain imported notes.
    """
    store = NoteStore()
    csv_path = tmp_path / "cli_load.csv"

    csv_path.write_text("id,text\n5,Loaded through CLI\n", encoding="utf-8")

    monkeypatch.setattr("builtins.input", lambda prompt: str(csv_path))

    load_from_csv(store)

    captured = capsys.readouterr()

    assert store.list_notes() == [{"id": 5, "text": "Loaded through CLI"}]
    assert "Notes loaded from CSV." in captured.out


def test_cli_save_without_source_prints_error(capsys):
    """
    Verify that CLI save handles missing source/target.

    Arrange: Create a store without a selected source.
    Act: Call save.
    Assert: The CLI should print a clear error.
    """
    store = NoteStore()

    save(store)

    captured = capsys.readouterr()

    assert "Error saving notes:" in captured.out