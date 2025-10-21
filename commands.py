from utils import (
    get_time, open_path, safe_eval, append_note, read_notes, get_sysinfo
)

NOTES_FILE = "data/notes.txt"

def cmd_help():
    return """
Available commands:
  help                  - Show this help menu
  time                  - Display current date & time
  open <path>           - Open a file or folder on your system
  note add "text"       - Add a note (stored in data/notes.txt)
  note show             - Display all notes
  calc <expression>     - Calculate a math expression (e.g. calc 2+3*4)
  sysinfo               - Show system information
  clear                 - Clear the screen
  exit                  - Exit the bot
"""

def cmd_time(_args):
    return get_time()

def cmd_open(args):
    if not args:
        return "Usage: open <path>"
    ok, msg = open_path(" ".join(args))
    return msg

def cmd_note(args):
    if not args:
        return "Usage: note add \"text\"  or note show"
    sub = args[0].lower()
    if sub == "add":
        text = " ".join(args[1:]).strip()
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        if not text:
            return "No text provided."
        append_note(NOTES_FILE, text)
        return "Note added."
    elif sub == "show":
        lines = read_notes(NOTES_FILE)
        if not lines:
            return "No notes found."
        return "".join(lines)
    else:
        return "Unknown note command. Use add or show."

def cmd_calc(args):
    if not args:
        return "Usage: calc <expression>"
    expr = " ".join(args)
    try:
        res = safe_eval(expr)
        return f"Result: {res}"
    except Exception as e:
        return f"Error: {e}"

def cmd_sysinfo(_args):
    info = get_sysinfo()
    lines = []
    lines.append(f"Platform: {info.get('platform')}")
    lines.append(f"Machine: {info.get('machine')}")
    lines.append(f"Processor: {info.get('processor')}")
    if "cpu_count_logical" in info:
        lines.append(f"CPU logical cores: {info.get('cpu_count_logical')}")
        lines.append(f"CPU physical cores: {info.get('cpu_count_physical')}")
        lines.append(f"CPU usage %: {info.get('cpu_usage_percent')}")
        lines.append(f"Memory: {info.get('memory_used_mb')}MB / {info.get('memory_total_mb')}MB ({info.get('memory_percent')}%)")
        lines.append(f"Disk: {info.get('disk_used_gb')}GB / {info.get('disk_total_gb')}GB ({info.get('disk_percent')}%)")
    return "\n".join(lines)

def cmd_clear():
    import os, platform
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    return ""
