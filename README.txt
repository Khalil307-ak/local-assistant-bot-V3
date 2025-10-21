# 🤖 Local Assistant Bot

A versatile command-line assistant written in **Python**. It provides essential system utilities and a simple, complete note-taking mechanism, all accessible directly from your terminal.

---

### 🌟 Features

* **Complete Note Management:** Add, view, and **delete** notes easily using simple commands.
* **System Utilities:** Get current time (`time`), view system usage/specs (`sysinfo`), and clear the screen (`clear`).
* **File Interaction:** Open files or directories on your system (`open <path>`).
* **Safe Calculator:** Evaluate arithmetic expressions directly (`calc <expression>`).
* **Cross-Platform:** Works on Windows, macOS, and Linux.

---

## 🛠️ Requirements & Setup

| Requirement | Details |
| :--- | :--- |
| **Python** | Version 3.8+ |
| **Dependencies** | [cite_start]`psutil` (for system information) [cite: 1] |

### Installation

1.  **Get the Files**
    ```bash
    git clone [https://github.com/YourUsername/local-assistant-bot.git](https://github.com/YourUsername/local-assistant-bot.git)
    cd local-assistant-bot
    ```

2.  **Optional: Create a Virtual Environment**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    source venv/bin/activate # On macOS/Linux
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Usage

Start the bot:
```bash
python main.py
Core CommandsCommandDescriptionExample UsagehelpShows the list of all available commands.>> helptimeDisplays the current date and time.>> timecalcCalculates a math expression safely.>> calc 1500 / 3.5 + 50openOpens a file or directory path.>> open "C:\Users\Documents\file.txt"sysinfoDisplays CPU, Memory, and Disk usage.>> sysinfo📝 Note Management (data/notes.txt)Notes are stored with a timestamp and accessed by index for deletion.Add a NoteBash>> note add "Remember to use the Xeon E3 for compiling."
Output: ✅ Note added to data/notes.txt.View All NotesBash>> note show
Example Output:📝 Your Notes:
----------------------------------------
  1. [2025-10-21 20:03:32] Finish Python project
  2. [2025-10-21 20:03:50] Remember to use the Xeon E3 for compiling.
----------------------------------------
Delete a NoteUse the index from the note show command. To delete note number 1:Bash>> note delete 1
Example Output:🗑️  Successfully deleted: [2025-10-21 20:03:32] Finish Python project
📂 File Structurelocal-assistant-bot/
│
├── main.py          # Bot entry point and command loop.
├── commands.py      # Implementation of all terminal commands (including note delete).
├── utils.py         # Helper functions for system and file operations.
├── requirements.txt # Project dependencies (psutil).
└── data/
    └── notes.txt    # Notes storage file (created automatically).
💡 Customization & NotesPerformance: Your Workstation HP Z210 with the Xeon E3-1240 and SSD/HDD combination is well-suited for running this local assistant quickly and efficiently.👨‍💻 Author & LicenseAuthor: KhalilLicense: MIT
