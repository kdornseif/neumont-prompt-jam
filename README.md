# Personal Notes App

A simple Python data-entry application for personal notes.

This version includes both:

1. A terminal-based CLI interface
2. A simple web interface using Flask

Both interfaces use the same shared note logic from `notes_core.py`.

## Current capabilities

The application can:

- Start with sample notes
- Add notes
- List notes
- Remove notes
- Load notes from a local CSV file
- Save notes back to the current CSV source/target
- Save notes as a new CSV file

## File structure

```text
personal_notes_app/
├── notes_core.py
├── notes_cli.py
├── notes_web.py
├── requirements.txt
├── README.md
└── summary.md