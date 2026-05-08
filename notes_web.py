"""
notes_web.py

Web interface for the Personal Notes App.

Version: 0.2.0

This version uses Flask because it is popular, beginner-friendly, and easy to
maintain for small Python web applications.

The web interface uses the same NoteStore class as the CLI application.
"""

from flask import Flask, redirect, render_template_string, request, url_for

from notes_core import APP_VERSION, NoteStore


app = Flask(__name__)

# For this beginner version, the app uses one shared in-memory NoteStore.
# This is simple and works for local development.
# A production multi-user app would need a different storage/session design.
store = NoteStore()


PAGE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Personal Notes App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            line-height: 1.5;
        }

        input[type="text"] {
            width: 70%;
            padding: 8px;
        }

        button {
            padding: 8px 12px;
            margin: 4px;
            cursor: pointer;
        }

        .section {
            border: 1px solid #ddd;
            padding: 16px;
            margin-bottom: 20px;
            border-radius: 8px;
        }

        .message {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 20px;
        }

        .note-row {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid #eee;
            padding: 8px 0;
        }

        .source-label {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Personal Notes App v{{ app_version }}</h1>

    <p>
        Current source/target:
        <span class="source-label">{{ source_label }}</span>
    </p>

    {% if message %}
        <div class="message">{{ message }}</div>
    {% endif %}

    <div class="section">
        <h2>Add Note</h2>

        <form method="post" action="{{ url_for('add_note') }}">
            <input type="text" name="note_text" placeholder="Enter a note">
            <button type="submit">Add Note</button>
        </form>
    </div>

    <div class="section">
        <h2>Notes</h2>

        {% if notes %}
            {% for note in notes %}
                <div class="note-row">
                    <span>{{ note["id"] }}. {{ note["text"] }}</span>

                    <form method="post" action="{{ url_for('remove_note') }}">
                        <input type="hidden" name="note_id" value="{{ note['id'] }}">
                        <button type="submit">Remove</button>
                    </form>
                </div>
            {% endfor %}
        {% else %}
            <p>No notes available.</p>
        {% endif %}
    </div>

    <div class="section">
        <h2>Load from CSV</h2>

        <form method="post" action="{{ url_for('load_csv') }}">
            <input type="text" name="file_path" placeholder="Example: notes.csv">
            <button type="submit">Load CSV</button>
        </form>
    </div>

    <div class="section">
        <h2>Save</h2>

        <form method="post" action="{{ url_for('save') }}">
            <button type="submit">Save to Current Source/Target</button>
        </form>
    </div>

    <div class="section">
        <h2>Save As CSV</h2>

        <form method="post" action="{{ url_for('save_as_csv') }}">
            <input type="text" name="file_path" placeholder="Example: notes.csv">
            <button type="submit">Save As CSV</button>
        </form>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    """
    Render the main web page.

    The page displays notes, source information, and forms for each action.
    """
    message = request.args.get("message", "")

    return render_template_string(
        PAGE_TEMPLATE,
        app_version=APP_VERSION,
        notes=store.list_notes(),
        source_label=store.get_source_label(),
        message=message
    )


@app.route("/add", methods=["POST"])
def add_note():
    """
    Add a note from the web form.

    After the action is complete, redirect back to the main page.
    """
    note_text = request.form.get("note_text", "")

    try:
        store.add_note(note_text)
        message = "Note added."
    except ValueError as error:
        message = f"Error: {error}"

    return redirect(url_for("index", message=message))


@app.route("/remove", methods=["POST"])
def remove_note():
    """
    Remove a note from the web form.

    The form sends the note ID as a hidden field.
    """
    note_id_text = request.form.get("note_id", "")

    try:
        note_id = int(note_id_text)
        removed_note = store.remove_note(note_id)
        message = f'Removed note: "{removed_note["text"]}"'
    except Exception as error:
        message = f"Error: {error}"

    return redirect(url_for("index", message=message))


@app.route("/load-csv", methods=["POST"])
def load_csv():
    """
    Load notes from a CSV path provided by the user.
    """
    file_path = request.form.get("file_path", "").strip()

    try:
        store.load_from_csv(file_path)
        message = "Notes loaded from CSV."
    except Exception as error:
        message = f"Error loading CSV: {error}"

    return redirect(url_for("index", message=message))


@app.route("/save", methods=["POST"])
def save():
    """
    Save notes to the currently selected source/target.
    """
    try:
        store.save()
        message = "Notes saved."
    except Exception as error:
        message = f"Error saving notes: {error}"

    return redirect(url_for("index", message=message))


@app.route("/save-as-csv", methods=["POST"])
def save_as_csv():
    """
    Save notes to a new CSV path provided by the user.
    """
    file_path = request.form.get("file_path", "").strip()

    try:
        store.save_as_csv(file_path)
        message = "Notes saved as CSV."
    except Exception as error:
        message = f"Error saving CSV: {error}"

    return redirect(url_for("index", message=message))


if __name__ == "__main__":
    app.run(debug=True)