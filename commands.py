from utils import (
    get_time, open_path, safe_eval, append_note, read_all_notes, get_sysinfo, delete_note_by_index
)

NOTES_FILE = "data/notes.txt"

def cmd_help():
    return """
Available commands:
  help                  - Show this help menu
  time                  - Display current date & time
  open <path>           - Open a file or folder on your system
  note add "text"       - Add a timestamped note
  note show             - Display all saved notes with indices
  note delete <index>   - Delete a specific note by its index
  calc <expression>     - Calculate a math expression (e.g. calc 2+3*4)
  sysinfo               - Show system hardware/performance information
  clear                 - Clear the screen
  exit / quit           - Exit the bot
"""

def cmd_time(_args):
    return get_time()

def cmd_open(args):
    if not args:
        return "Usage: open <path> (e.g. open C:\\Users\\...)"
    path = " ".join(args)
    ok, msg = open_path(path)
    return msg

def cmd_note(args):
    if not args:
        return "Usage: note add \"text\", note show, or note delete <index>"
    sub = args[0].lower()
    
    if sub == "add":
        text = " ".join(args[1:]).strip()
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        if not text:
            return "No text provided."
        append_note(NOTES_FILE, text)
        return f"✅ Note added to {NOTES_FILE}."
    
    elif sub == "show":
        notes = read_all_notes(NOTES_FILE)
        if not notes:
            return f"💡 No notes found in {NOTES_FILE}."
        
        # Display notes with 1-based index
        output = ["\n📝 Your Notes:", "-"*40]
        for index, line in enumerate(notes, 1):
            output.append(f"  {index}. {line.strip()}")
        output.append("-"*40)
        return "\n".join(output)
    
    elif sub == "delete":
        if len(args) < 2:
            return "Usage: note delete <index>. Use 'note show' to find the index."
        
        try:
            index = int(args[1])
        except ValueError:
            return f"❌ Invalid index: '{args[1]}'. Index must be a number."
            
        success, message = delete_note_by_index(NOTES_FILE, index)
        
        if success:
            return f"🗑️  Successfully deleted: {message}"
        else:
            return f"❌ {message}"
            
    else:
        return "Unknown note command. Use 'add', 'show', or 'delete'."

def cmd_calc(args):
    if not args:
        return "Usage: calc <expression> (e.g. calc 1500 / 3.5)"
    expr = " ".join(args)
    try:
        res = safe_eval(expr)
        return f"Result: {expr} = {res}"
    except ValueError as e:
        return f"Error: {e}"
    except Exception:
        return f"Error evaluating expression: {expr}"

def cmd_sysinfo(_args):
    info = get_sysinfo()
    lines = []
    lines.append("🤖 System Information:")
    lines.append(f"  Platform: {info.get('platform')}")
    lines.append(f"  Machine: {info.get('machine')}")
    lines.append(f"  Processor: {info.get('processor')}")
    lines.append("-" * 30)
    
    if "cpu_count_logical" in info:
        lines.append(f"  CPU Cores (Logical/Physical): {info.get('cpu_count_logical')}/{info.get('cpu_count_physical')}")
        lines.append(f"  CPU Usage: {info.get('cpu_usage_percent')}%")
        lines.append(f"  Memory (RAM): {info.get('memory_used_mb')}MB / {info.get('memory_total_mb')}MB ({info.get('memory_percent')}%)")
        lines.append(f"  Disk Usage: {info.get('disk_used_gb')}GB / {info.get('disk_total_gb')}GB ({info.get('disk_percent')}%)")
    lines.append("-" * 30)
    
    # Personalized hint
    lines.append("💡 Your Xeon E3-1240 and 8GB RAM are handling tasks smoothly. GT 740 is ready for simple CUDA jobs!")
    
    return "\n".join(lines)

def cmd_clear():
    import os, platform
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    return ""
