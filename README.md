# Personal Notes App

Version: 0.2.0

A simple Python data-entry application for personal notes.

This version includes:

1. A terminal-based CLI interface
2. A simple web interface using Flask
3. Shared note logic
4. CSV load/save support
5. A pytest regression test suite
6. Release notes

## Current capabilities

The application can:

- Start with sample notes
- Add notes
- List notes
- Remove notes
- Load notes from a local CSV file
- Save notes back to the current CSV source/target
- Save notes as a new CSV file
- Run through a terminal interface
- Run through a web browser
- Run automated tests for core, CLI, and web behavior

## File structure

```text
personal_notes_app/
├── notes_core.py
├── notes_cli.py
├── notes_web.py
├── requirements.txt
├── README.md
├── summary.md
├── release_notes.md
└── tests/
    ├── test_notes_core.py
    ├── test_notes_cli.py
    └── test_notes_web.py