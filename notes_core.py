"""
notes_core.py

Shared application logic for the Personal Notes App.

Version: 0.2.0

Both the CLI application and the web application import this file so that:
1. Notes are represented the same way.
2. CSV loading and saving work the same way.
3. Add/list/remove behavior stays consistent across interfaces.

This keeps the business logic in one place and prevents the CLI and web app
from slowly drifting apart.
"""

import csv
from pathlib import Path


APP_VERSION = "0.2.0"


class NoteStore:
    """
    Manage notes and optional CSV persistence.

    This class holds the current in-memory notes and tracks the currently
    selected source/target file path.

    For now, CSV is the only supported source type.
    Later, other source types could be added, such as JSON, SQLite, or an API.
    """

    def __init__(self):
        """
        Create a new NoteStore with starter notes.

        The notes begin in memory only. They are not connected to a CSV file
        until the user loads from a CSV file or saves as a CSV file.
        """
        self.notes = [
            {"id": 1, "text": "Review Python functions"},
            {"id": 2, "text": "Practice using lists"},
            {"id": 3, "text": "Build a CLI and web version"}
        ]

        # The source type is None until a file is loaded or selected.
        self.source_type = None

        # The source path is None until the user loads from or saves to a CSV.
        self.source_path = None

        # Track the next note ID so each note can have a stable identifier.
        self.next_id = 4

    def list_notes(self):
        """
        Return all notes.

        A shallow copy is returned so callers can read the notes without
        accidentally replacing the internal list object.
        """
        return list(self.notes)

    def add_note(self, text):
        """
        Add a new note and return the created note.

        Blank notes are rejected because they are usually accidental input.
        """
        cleaned_text = text.strip()

        if cleaned_text == "":
            raise ValueError("Note text cannot be empty.")

        note = {
            "id": self.next_id,
            "text": cleaned_text
        }

        self.notes.append(note)
        self.next_id += 1

        return note

    def remove_note(self, note_id):
        """
        Remove a note by ID.

        Returns the removed note.

        Raises ValueError if no note with that ID exists.
        """
        for index, note in enumerate(self.notes):
            if note["id"] == note_id:
                return self.notes.pop(index)

        raise ValueError(f"No note found with ID {note_id}.")

    def load_from_csv(self, file_path):
        """
        Load notes from a CSV file.

        Expected CSV format:

        id,text
        1,Example note
        2,Another note

        If the CSV does not exist, this method raises FileNotFoundError.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"CSV file does not exist: {file_path}")

        loaded_notes = []

        with path.open(mode="r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)

            # Validate that the CSV has the expected columns.
            if reader.fieldnames is None or "id" not in reader.fieldnames or "text" not in reader.fieldnames:
                raise ValueError("CSV must contain 'id' and 'text' columns.")

            for row in reader:
                note_id_text = row["id"].strip()
                note_text = row["text"].strip()

                # Empty rows are skipped rather than causing the entire load to fail.
                if note_id_text == "" or note_text == "":
                    continue

                loaded_notes.append({
                    "id": int(note_id_text),
                    "text": note_text
                })

        self.notes = loaded_notes
        self.source_type = "csv"
        self.source_path = str(path)

        # Keep future note IDs higher than any existing note ID.
        if self.notes:
            self.next_id = max(note["id"] for note in self.notes) + 1
        else:
            self.next_id = 1

    def save(self):
        """
        Save notes back to the currently selected source.

        This requires the user to have already loaded from a CSV or saved as CSV.
        """
        if self.source_type != "csv" or self.source_path is None:
            raise ValueError("No CSV source/target is currently selected. Use save_as_csv first.")

        self.save_as_csv(self.source_path)

    def save_as_csv(self, file_path):
        """
        Save notes to a new or existing CSV file.

        This also updates the current source/target so future saves go to this path.
        """
        path = Path(file_path)

        with path.open(mode="w", newline="", encoding="utf-8") as csv_file:
            fieldnames = ["id", "text"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()

            for note in self.notes:
                writer.writerow(note)

        self.source_type = "csv"
        self.source_path = str(path)

    def get_source_label(self):
        """
        Return a human-friendly description of the current source/target.
        """
        if self.source_type is None or self.source_path is None:
            return "No source selected"

        return f"{self.source_type}: {self.source_path}"