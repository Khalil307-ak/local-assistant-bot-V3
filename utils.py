import os
import platform
import subprocess
import shlex
import datetime
import psutil

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def open_path(path: str):
    path = path.strip('"').strip("'")
    if not os.path.exists(path):
        return False, f"Path not found: {path}"
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return True, f"Opened: {path}"
    except Exception as e:
        return False, f"Error opening file: {e}"

def safe_eval(expr: str):
    """Safe arithmetic evaluator"""
    allowed = "0123456789+-*/%(). eE"
    for ch in expr:
        if ch not in allowed:
            raise ValueError("Expression contains invalid characters.")
    try:
        result = eval(expr, {"__builtins__": None}, {})
        return result
    except Exception as e:
        raise ValueError(f"Cannot evaluate expression: {e}")

def append_note(file_path: str, text: str):
    # Ensure the directory exists (e.g., 'data/')
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{ts}] {text}\n")
    return True

# --- NEW/UPDATED NOTE FUNCTIONS ---

def read_all_notes(file_path: str):
    """Reads all notes and returns them as a list of strings."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        # returns list of lines, including newline characters
        return f.readlines()

def delete_note_by_index(file_path: str, index: int):
    """Deletes a note by its 1-based index and rewrites the file."""
    notes = read_all_notes(file_path)
    
    # Adjust index from 1-based (user input) to 0-based (list index)
    index_to_delete = index - 1 
    
    if 0 <= index_to_delete < len(notes):
        deleted_note = notes.pop(index_to_delete).strip() # Remove and get the note content
        
        # Rewrite the entire file with the remaining notes
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(notes)
            
        return True, deleted_note
    else:
        return False, f"Error: Note number {index} not found."

# --- END NOTE FUNCTIONS ---

def get_sysinfo():
    info = {}
    try:
        info["platform"] = platform.platform()
        info["machine"] = platform.machine()
        info["processor"] = platform.processor()
        info["cpu_count_logical"] = psutil.cpu_count(logical=True)
        info["cpu_count_physical"] = psutil.cpu_count(logical=False)
        info["cpu_usage_percent"] = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        info["memory_total_mb"] = round(mem.total/1024/1024, 1)
        info["memory_used_mb"] = round(mem.used/1024/1024, 1)
        info["memory_percent"] = mem.percent
        disk = psutil.disk_usage(".")
        info["disk_total_gb"] = round(disk.total/1024/1024/1024, 1)
        info["disk_used_gb"] = round(disk.used/1024/1024/1024, 1)
        info["disk_percent"] = disk.percent
    except Exception:
        info["platform"] = platform.platform()
        info["machine"] = platform.machine()
        info["processor"] = platform.processor()
    return info
