---

## File: `release_notes.md`

```markdown
# Release Notes

This file is append-only.

Do not rewrite prior version sections except to correct obvious spelling or formatting mistakes.

Each release should add a new section at the top with:

- Version
- Date
- Functional changes
- Non-functional changes
- Files changed
- Testing notes
- Known limitations

This project uses a simple Semantic Versioning-inspired format:

```text
MAJOR.MINOR.PATCH

Version 0.2.0 - Test Coverage and Release Notes

Date: 2026-05-07

Functional changes
Added a pytest regression test suite.
Added tests for shared core note functionality.
Added tests for CLI interactions.
Added tests for Flask web interactions.
Added application version metadata through APP_VERSION.
Added visible version display in the CLI menu.
Added visible version display in the web page heading.

Non-functional changes
Added release notes as an append-only project artifact.
Added a simple versioning convention based on MAJOR.MINOR.PATCH.
Added testing guidance based on the Arrange / Act / Assert pattern.
Added pytest to project dependencies.
Updated documentation to explain how to run tests.
Updated documentation to explain the release notes and versioning approach.

Files changed
notes_core.py
notes_cli.py
notes_web.py
requirements.txt
README.md
summary.md
release_notes.md
tests/test_notes_core.py
tests/test_notes_cli.py
tests/test_notes_web.py

Testing notes

The test suite now covers:
Starter note creation
Adding notes
Rejecting blank notes
Removing notes
Missing note removal
CSV save-as
CSV save to current source
CSV load
Missing CSV file
Invalid CSV columns
CLI list/add/remove/load/save interactions
Web page rendering
Web add/remove/load/save interactions
Common web and CLI error messages

Known limitations
GitHub Actions CI has not been added yet.
CSV duplicate ID validation has not been added yet.
CSV non-numeric ID validation has not been made user-friendly yet.
Version values are manually updated across files.
The web app still uses a single shared in-memory store for local learning simplicity.

Version 0.1.0 - Initial End-to-End Application

Date: 2026-05-07

Functional changes
Added shared note logic.
Added terminal-based CLI interface.
Added Flask-based web interface.
Added starter notes.
Added add note behavior.
Added list note behavior.
Added remove note behavior.
Added CSV load behavior.
Added CSV save behavior.
Added CSV save-as behavior.

Non-functional changes
Added project README.
Added application summary.
Separated shared logic from interface-specific code.
Chose Flask as a beginner-friendly web framework.

Files changed
notes_core.py
notes_cli.py
notes_web.py
requirements.txt
README.md
summary.md

Testing notes
Manual testing only.
No automated regression tests in this version.

Known limitations
No automated tests.
No edit-note feature.
No search feature.
No timestamps.
No tags or categories.
No login or multi-user support.