# Local Assistant Bot

A simple local command-line assistant written in Python. It allows you to manage quick notes directly from your terminal — add, list, and delete notes — all saved locally on your computer.

## Features

* Add new notes quickly from the terminal.
* View all saved notes.
* Delete specific notes by index.
* Data saved locally in a JSON file (`notes.json`).

## Requirements

* Python 3.8+
* Windows / macOS / Linux

## Installation

```bash
# 1. Clone the repository or copy the files
cd C:\Users\Khali\OneDrive\Desktop\local-assistant-bot

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# 3. Install dependencies (if any in future)
pip install -r requirements.txt
```

## Usage

### Add a note

```bash
python main.py add "Buy milk"
```

### List all notes

```bash
python main.py list
```

### Delete a note

```bash
python main.py delete 1
```

## Example Output

```bash
$ python main.py add "Finish Python project"
✅ Note added: Finish Python project

$ python main.py list
1. Finish Python project
2. Buy milk

$ python main.py delete 1
🗑️  Deleted note: Finish Python project
```

## File Structure

```
local-assistant-bot/
│
├── main.py          # Main bot script
├── notes.json       # Data storage (created automatically)
├── README.md        # Project documentation
└── requirements.txt # Future dependencies
```

## Notes

* You can rename the script (`main.py`) to `note.py` for easier use, like:

  ```bash
  python note.py add "Buy milk"
  ```
* To use `note` directly as a command (without `python`), you can add an alias or rename it as an executable script.

## Future Improvements

* Add search functionality for notes.
* Add a reminder or notification system.
* Optional voice assistant integration.

---

**Author:** Khalil
**License:** MIT
