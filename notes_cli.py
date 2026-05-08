"""
notes_cli.py

Terminal interface for the Personal Notes App.

Version: 0.2.0

This file handles user interaction through the command line.

The actual note logic lives in notes_core.py so that the CLI and web interface
can share the same behavior.
"""

from notes_core import APP_VERSION, NoteStore


def show_menu(store):
    """
    Display the CLI menu.

    The current source/target is shown so the user knows where save will write.
    """
    print(f"\nPersonal Notes App - CLI v{APP_VERSION}")
    print("------------------------")
    print(f"Current source/target: {store.get_source_label()}")
    print("1. List notes")
    print("2. Add note")
    print("3. Remove note")
    print("4. Load from CSV")
    print("5. Save")
    print("6. Save as CSV")
    print("7. Quit")


def list_notes(store):
    """
    Print all notes in the terminal.
    """
    notes = store.list_notes()

    if len(notes) == 0:
        print("\nNo notes available.")
        return

    print("\nYour notes:")

    for note in notes:
        print(f"{note['id']}. {note['text']}")


def add_note(store):
    """
    Ask the user for note text and add it through the shared NoteStore.
    """
    text = input("\nEnter your note: ")

    try:
        store.add_note(text)
        print("Note added.")
    except ValueError as error:
        print(f"Error: {error}")


def remove_note(store):
    """
    Ask the user for a note ID and remove it through the shared NoteStore.
    """
    list_notes(store)

    note_id_text = input("\nEnter the ID of the note to remove: ").strip()

    if not note_id_text.isdigit():
        print("Please enter a valid numeric note ID.")
        return

    note_id = int(note_id_text)

    try:
        removed_note = store.remove_note(note_id)
        print(f'Removed note: "{removed_note["text"]}"')
    except ValueError as error:
        print(f"Error: {error}")


def load_from_csv(store):
    """
    Ask the user for a CSV path and load notes from that file.
    """
    file_path = input("\nEnter CSV file path to load: ").strip()

    try:
        store.load_from_csv(file_path)
        print("Notes loaded from CSV.")
    except Exception as error:
        print(f"Error loading CSV: {error}")


def save(store):
    """
    Save notes to the currently selected source/target.
    """
    try:
        store.save()
        print("Notes saved.")
    except Exception as error:
        print(f"Error saving notes: {error}")


def save_as_csv(store):
    """
    Ask the user for a CSV path and save notes to that file.
    """
    file_path = input("\nEnter CSV file path to save as: ").strip()

    try:
        store.save_as_csv(file_path)
        print("Notes saved as CSV.")
    except Exception as error:
        print(f"Error saving CSV: {error}")


def run_cli():
    """
    Run the CLI application loop.
    """
    store = NoteStore()

    while True:
        show_menu(store)

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            list_notes(store)
        elif choice == "2":
            add_note(store)
        elif choice == "3":
            remove_note(store)
        elif choice == "4":
            load_from_csv(store)
        elif choice == "5":
            save(store)
        elif choice == "6":
            save_as_csv(store)
        elif choice == "7":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    run_cli()