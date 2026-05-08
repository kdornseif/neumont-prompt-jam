"""
tests/test_notes_core.py

Tests for shared note logic.

Version: 0.2.0

Testing guideline used:
Arrange / Act / Assert.

Pytest's documentation describes tests as having an arrange phase, an act phase,
and an assert phase. This keeps each test focused on one behavior.

These tests focus on notes_core.py because both the CLI and web interfaces
depend on this shared logic.
"""

import csv

import pytest

from notes_core import APP_VERSION, NoteStore


def test_app_version_is_current():
    """
    Verify that the application version matches the release notes version.

    Arrange: Use the imported APP_VERSION.
    Act: Compare it to the expected version.
    Assert: The version should be 0.2.0.
    """
    assert APP_VERSION == "0.2.0"


def test_store_starts_with_three_sample_notes():
    """
    Verify that a new store starts with sample notes.

    Arrange: Create a new NoteStore.
    Act: List the notes.
    Assert: There should be three starter notes.
    """
    store = NoteStore()

    notes = store.list_notes()

    assert len(notes) == 3
    assert notes[0]["id"] == 1
    assert notes[0]["text"] == "Review Python functions"


def test_add_note_adds_trimmed_note_with_next_id():
    """
    Verify that adding a note trims whitespace and assigns the next ID.

    Arrange: Create a new NoteStore.
    Act: Add a note with extra whitespace.
    Assert: The stored note should be cleaned and assigned ID 4.
    """
    store = NoteStore()

    note = store.add_note("  Learn pytest  ")

    assert note == {"id": 4, "text": "Learn pytest"}
    assert store.list_notes()[-1] == {"id": 4, "text": "Learn pytest"}


def test_add_blank_note_raises_value_error():
    """
    Verify that blank notes are rejected.

    Arrange: Create a new NoteStore.
    Act and Assert: Adding a blank note should raise ValueError.
    """
    store = NoteStore()

    with pytest.raises(ValueError, match="Note text cannot be empty"):
        store.add_note("   ")


def test_remove_note_removes_matching_id():
    """
    Verify that removing a note by ID removes the correct note.

    Arrange: Create a new NoteStore.
    Act: Remove note ID 2.
    Assert: The removed note should match ID 2 and no longer appear in the list.
    """
    store = NoteStore()

    removed_note = store.remove_note(2)

    remaining_ids = [note["id"] for note in store.list_notes()]

    assert removed_note == {"id": 2, "text": "Practice using lists"}
    assert 2 not in remaining_ids


def test_remove_missing_note_raises_value_error():
    """
    Verify that removing an unknown ID fails clearly.

    Arrange: Create a new NoteStore.
    Act and Assert: Removing a missing ID should raise ValueError.
    """
    store = NoteStore()

    with pytest.raises(ValueError, match="No note found with ID 999"):
        store.remove_note(999)


def test_get_source_label_without_source():
    """
    Verify the source label before any file is selected.

    Arrange: Create a new NoteStore.
    Act: Get the source label.
    Assert: The label should indicate that no source is selected.
    """
    store = NoteStore()

    label = store.get_source_label()

    assert label == "No source selected"


def test_save_without_source_raises_value_error():
    """
    Verify that save fails before a source/target is selected.

    Arrange: Create a new NoteStore.
    Act and Assert: Saving should raise ValueError.
    """
    store = NoteStore()

    with pytest.raises(ValueError, match="No CSV source/target is currently selected"):
        store.save()


def test_save_as_csv_writes_notes_and_updates_source(tmp_path):
    """
    Verify that save-as writes a CSV file and updates the selected source.

    Arrange: Create a new NoteStore and choose a temporary CSV path.
    Act: Save as CSV.
    Assert: The file should exist and source metadata should point to it.
    """
    store = NoteStore()
    csv_path = tmp_path / "notes.csv"

    store.save_as_csv(csv_path)

    assert csv_path.exists()
    assert store.source_type == "csv"
    assert store.source_path == str(csv_path)

    with csv_path.open(mode="r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    assert rows[0] == {"id": "1", "text": "Review Python functions"}
    assert rows[1] == {"id": "2", "text": "Practice using lists"}
    assert rows[2] == {"id": "3", "text": "Build a CLI and web version"}


def test_load_from_csv_replaces_notes_and_updates_next_id(tmp_path):
    """
    Verify that loading from CSV replaces current notes.

    Arrange: Create a temporary CSV file with two notes.
    Act: Load the CSV.
    Assert: The store should contain the CSV notes and next ID should be 12.
    """
    csv_path = tmp_path / "loaded_notes.csv"

    csv_path.write_text(
        "id,text\n10,Imported note\n11,Another imported note\n",
        encoding="utf-8"
    )

    store = NoteStore()

    store.load_from_csv(csv_path)

    assert store.list_notes() == [
        {"id": 10, "text": "Imported note"},
        {"id": 11, "text": "Another imported note"}
    ]
    assert store.next_id == 12
    assert store.source_type == "csv"
    assert store.source_path == str(csv_path)


def test_load_from_missing_csv_raises_file_not_found(tmp_path):
    """
    Verify that loading a missing CSV file fails clearly.

    Arrange: Create a path that does not exist.
    Act and Assert: Loading should raise FileNotFoundError.
    """
    missing_path = tmp_path / "missing.csv"
    store = NoteStore()

    with pytest.raises(FileNotFoundError):
        store.load_from_csv(missing_path)


def test_load_from_csv_with_missing_columns_raises_value_error(tmp_path):
    """
    Verify that CSV files must include id and text columns.

    Arrange: Create a CSV with incorrect columns.
    Act and Assert: Loading should raise ValueError.
    """
    csv_path = tmp_path / "bad_columns.csv"
    csv_path.write_text("wrong,columns\n1,hello\n", encoding="utf-8")

    store = NoteStore()

    with pytest.raises(ValueError, match="CSV must contain 'id' and 'text' columns"):
        store.load_from_csv(csv_path)


def test_save_writes_back_to_current_source(tmp_path):
    """
    Verify that save writes back to the selected CSV source.

    Arrange: Save as CSV once to establish the source.
    Act: Add a note and call save.
    Assert: The CSV file should include the new note.
    """
    csv_path = tmp_path / "notes.csv"
    store = NoteStore()

    store.save_as_csv(csv_path)
    store.add_note("Saved later")
    store.save()

    loaded_store = NoteStore()
    loaded_store.load_from_csv(csv_path)

    assert loaded_store.list_notes()[-1] == {"id": 4, "text": "Saved later"}