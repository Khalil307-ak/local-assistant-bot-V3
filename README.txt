ocal Assistant Bot (v2.0) - The Advanced Local Assistant

A comprehensive and advanced assistant operated via the Terminal, written in Python. It has been developed as an integrated tool for task management, calculations, system monitoring, and adding a touch of fun to your daily experience.

🌟 Key Features in Version 2.0

Comprehensive Note Management: Add, show, search by keyword, edit, and delete individually or in bulk.

Advanced System Tools: Battery check (for laptops), local network info (IP and Wi-Fi), and quick system cleanup tasks.

Extended Calculation Functions: Safe calculator, saving calculation history, and unit conversions (length, weight, temperature).

Enhanced Interactivity: Colored user interface using the rich library, along with an initial welcome ASCII Banner.

Entertainment & Reminders: Random generator (passwords, numbers), quotes/jokes, and the ability to send desktop notifications as reminders.

🛠️ Requirements and Setup

Requirement

Details

Python

Version 3.8 and above.

Libraries

psutil, rich, requests, plyer (Required for new functions).

Project Structure

local-assistant-bot/
│
├── main.py          # Bot entry point, command processing, and interface display.
├── commands.py      # Implementation of all terminal commands (with color formatting).
├── utils.py         # Helper functions (system, calculation, notes, conversion).
├── requirements.txt # List of required dependencies.
└── data/
    ├── notes.txt    # Note storage file.
    └── calc_history.txt # Calculation history storage file.



Installation Steps

Navigate to the project folder:

cd local-assistant-bot



Install all required libraries:

pip install -r requirements.txt



🚀 Quick Usage Guide

Start the bot:

python main.py



Note: Commands are not case-sensitive (you can type help or HELP).

📝 Note Management

Command

Description

Example Usage

note add

Adds a new timestamped note.

note add "Reminder: Finish backend code today"

note show

Displays all notes with their index.

note show

note search

Searches for notes containing a specific keyword.

note search "Python"

note edit

Edits the content of a note using its index number.

note edit 3 "New text for the edit"

note delete

Deletes a note by index, or deletes all notes containing a keyword.

note delete 5 or note delete "old"

💻 System Tools and Monitoring

Command

Description

Example Usage

sysinfo

Displays details of CPU (Xeon E3) consumption, memory, and storage.

sysinfo

clean

Cleans temporary files and caches (Windows/Linux/macOS).

clean

battery

Checks battery status, charge level, and remaining time (for laptops).

battery

network

Displays local IP address and Wi-Fi network name (SSID).

network

remind

Sets a desktop notification to appear after a specified number of seconds.

remind 300 "Coffee break time"

🧮 Calculations and Fun

Command

Description

Example Usage

calc

Safe arithmetic calculator.

calc (500 + 3.14) * 2

calc history

Displays the last 10 calculation entries.

calc history

convert

Converts units (length, weight, temp).

convert length 10 km to mi

random

Generates random numbers or strings (e.g., passwords).

random string 16 or random number 1 100

fun quote

Fetches a random programming quote.

fun quote

fun joke

Displays a short local joke.

fun joke

💡 Notes and Personalization

Performance: The bot is designed to run efficiently on your HP Z210 system, leveraging the power of the Xeon E3-1240 processor and fast storage (SSD/HDD).

Colors: All outputs use the rich library to provide distinct and easy-to-read coloring.

Notifications: The remind feature relies on the plyer library, and may require installing local OS dependencies (like pynotify on Linux) to function fully.
