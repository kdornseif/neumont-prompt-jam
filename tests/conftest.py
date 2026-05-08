"""
tests/conftest.py

Pytest configuration for the Personal Notes App.

Version: 0.2.1

Purpose:
This file makes sure the project root folder is available on Python's import path
when pytest runs.

Why this is needed:
The application files are stored at the project root:

- notes_core.py
- notes_cli.py
- notes_web.py

The test files are stored in the tests/ folder.

In some local environments, pytest may collect the tests successfully but not
automatically make the project root importable. When that happens, imports such
as the following can fail:

from notes_core import NoteStore

This conftest.py file fixes that by adding the project root to sys.path before
test modules are imported.
"""

import sys
from pathlib import Path


# __file__ points to this file:
# tests/conftest.py
#
# parent gives:
# tests/
#
# parent.parent gives:
# the project root folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Add the project root to Python's import path if it is not already present.
# This lets tests import root-level files such as notes_core.py.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))