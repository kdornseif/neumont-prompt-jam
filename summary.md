
### File: `summary.md`

```markdown
# Application Summary

## Application Name

Personal Notes App

## Current Version Scope

This is a simple terminal-based Python data-entry application for personal notes.

## Capabilities

The application currently supports:

1. Listing notes  
   The user can view all notes currently stored in the session.

2. Adding notes  
   The user can enter a new note through the terminal.

3. Removing notes  
   The user can remove a note by choosing its displayed number.

4. Starting with sample notes  
   The application begins with three sample notes so the user can immediately test listing and removal.

5. Running in a terminal  
   The application does not require a graphical interface.

## Data Storage

Notes are stored in a Python list.

Each note is currently stored as a plain string.

Example:

```python
notes = [
    "Review Python functions",
    "Practice using lists",
    "Write a small terminal app"
]