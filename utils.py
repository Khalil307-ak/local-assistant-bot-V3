import os
import platform
import subprocess
import datetime
import psutil
import requests
import random
import time
from math import pi

# --- CONSTANTS ---
NOTES_FILE = "data/notes.txt"
CALC_HISTORY_FILE = "data/calc_history.txt"
# Conversion factors (example set)
CONVERSION_FACTORS = {
    "length": {"km_to_mi": 0.621371, "m_to_ft": 3.28084, "cm_to_in": 0.393701},
    "weight": {"kg_to_lb": 2.20462, "g_to_oz": 0.035274},
    "temp": {"C_to_F": lambda c: (c * 9/5) + 32, "F_to_C": lambda f: (f - 32) * 5/9},
}

# --- TIME & SYSTEM UTILITIES ---

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

# --- CALC UTILITIES ---

def safe_eval(expr: str):
    """Safe arithmetic evaluator"""
    allowed = "0123456789+-*/%(). eE"
    for ch in expr:
        if ch not in allowed:
            raise ValueError("Expression contains invalid characters.")
    # Add common constants for better calc (e.g. pi)
    local_scope = {"__builtins__": None, "pi": pi}
    try:
        result = eval(expr, local_scope, {})
        save_calc_history(f"{expr} = {result}")
        return result
    except Exception as e:
        raise ValueError(f"Cannot evaluate expression: {e}")

def save_calc_history(entry: str):
    os.makedirs(os.path.dirname(CALC_HISTORY_FILE) or ".", exist_ok=True)
    with open(CALC_HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
    
    # Keep only the last 10 entries
    with open(CALC_HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    if len(lines) > 10:
        with open(CALC_HISTORY_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines[-10:]) # Keep only the last 10

def read_calc_history():
    if not os.path.exists(CALC_HISTORY_FILE):
        return []
    with open(CALC_HISTORY_FILE, "r", encoding="utf-8") as f:
        return f.readlines()

def convert_unit(type: str, value: float, unit_from: str, unit_to: str):
    key = f"{unit_from}_to_{unit_to}"
    
    if type == 'temp':
        if unit_from == 'C' and unit_to == 'F':
            return CONVERSION_FACTORS['temp']['C_to_F'](value)
        elif unit_from == 'F' and unit_to == 'C':
            return CONVERSION_FACTORS['temp']['F_to_C'](value)
        else:
            raise ValueError("Unsupported temperature conversion.")

    if type in CONVERSION_FACTORS and key in CONVERSION_FACTORS[type]:
        return value * CONVERSION_FACTORS[type][key]
    else:
        # Check reverse conversion
        rev_key = f"{unit_to}_to_{unit_from}"
        if type in CONVERSION_FACTORS and rev_key in CONVERSION_FACTORS[type]:
            return value / CONVERSION_FACTORS[type][rev_key]
        else:
            raise ValueError(f"Unsupported conversion type/units: {type} {unit_from} to {unit_to}")

# --- NOTE UTILITIES ---

def read_all_notes(file_path: str):
    """Reads all notes and returns them as a list of strings with indices."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        # returns list of lines, including newline characters
        return f.readlines()

def append_note(file_path: str, text: str):
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        ts = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        f.write(ts + text + "\n")

def save_notes_list(file_path: str, notes_list: list):
    """Rewrites the file with a list of notes."""
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(notes_list)

def delete_note_by_index(index: int):
    notes = read_all_notes(NOTES_FILE)
    index_to_delete = index - 1 
    
    if 0 <= index_to_delete < len(notes):
        deleted_note = notes.pop(index_to_delete).strip()
        save_notes_list(NOTES_FILE, notes)
        return True, deleted_note
    else:
        return False, f"Note number {index} not found."

def search_notes(keyword: str):
    """Returns a list of notes containing the keyword and their 1-based index."""
    notes = read_all_notes(NOTES_FILE)
    results = []
    keyword_lower = keyword.lower()
    for index, note in enumerate(notes, 1):
        if keyword_lower in note.lower():
            results.append((index, note.strip()))
    return results

def delete_notes_by_keyword(keyword: str):
    """Deletes all notes containing the keyword."""
    notes = read_all_notes(NOTES_FILE)
    original_count = len(notes)
    
    # Filter out notes containing the keyword
    notes_to_keep = [note for note in notes if keyword.lower() not in note.lower()]
    
    deleted_count = original_count - len(notes_to_keep)
    
    if deleted_count > 0:
        save_notes_list(NOTES_FILE, notes_to_keep)
    
    return deleted_count

def edit_note_by_index(index: int, new_text: str):
    notes = read_all_notes(NOTES_FILE)
    index_to_edit = index - 1
    
    if 0 <= index_to_edit < len(notes):
        # Extract the timestamp part
        old_note = notes[index_to_edit].strip()
        timestamp = old_note.split(']')[0] + ']' if ']' in old_note else f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
        
        # Replace the note with the old timestamp + new text
        notes[index_to_edit] = f"{timestamp} {new_text}\n"
        save_notes_list(NOTES_FILE, notes)
        return True, old_note
    else:
        return False, f"Note number {index} not found."

# --- ADVANCED SYSTEM UTILITIES ---

def get_sysinfo():
    """Returns system information including CPU, memory, and disk usage."""
    try:
        # Get basic system info
        platform_name = platform.system()
        machine = platform.machine()
        processor = platform.processor()
        
        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Get memory info
        memory = psutil.virtual_memory()
        memory_used_mb = round(memory.used / (1024 * 1024), 1)
        memory_total_mb = round(memory.total / (1024 * 1024), 1)
        memory_percent = memory.percent
        
        # Get disk info
        disk = psutil.disk_usage('/')
        disk_used_gb = round(disk.used / (1024 * 1024 * 1024), 1)
        disk_total_gb = round(disk.total / (1024 * 1024 * 1024), 1)
        disk_percent = round((disk.used / disk.total) * 100, 1)
        
        return {
            'platform': platform_name,
            'machine': machine,
            'processor': processor,
            'cpu_usage_percent': cpu_percent,
            'memory_used_mb': memory_used_mb,
            'memory_total_mb': memory_total_mb,
            'memory_percent': memory_percent,
            'disk_used_gb': disk_used_gb,
            'disk_total_gb': disk_total_gb,
            'disk_percent': disk_percent
        }
    except Exception as e:
        return {
            'platform': 'Unknown',
            'machine': 'Unknown',
            'processor': 'Unknown',
            'cpu_usage_percent': 'N/A',
            'memory_used_mb': 'N/A',
            'memory_total_mb': 'N/A',
            'memory_percent': 'N/A',
            'disk_used_gb': 'N/A',
            'disk_total_gb': 'N/A',
            'disk_percent': 'N/A'
        }

def clean_system():
    """Tries to clean temp files and caches (basic, cross-platform friendly)."""
    if platform.system() == "Windows":
        # Note: Cleaning recycle bin is complex and requires elevated rights or external tools.
        # Focusing on system and user temporary files.
        temp_dirs = [
            os.environ.get('TEMP'),
            os.environ.get('TMP'),
            os.path.join(os.environ.get('WINDIR'), 'Temp')
        ]
        
        cleaned_files = 0
        for temp_dir in temp_dirs:
            if temp_dir and os.path.exists(temp_dir):
                for item in os.listdir(temp_dir):
                    # Only delete files older than 7 days to avoid current conflicts
                    full_path = os.path.join(temp_dir, item)
                    try:
                        if os.path.isfile(full_path) and (time.time() - os.path.getmtime(full_path)) > 7 * 86400:
                            os.remove(full_path)
                            cleaned_files += 1
                        elif os.path.isdir(full_path) and item not in ['..', '.']:
                             # Simple directory removal
                             pass
                    except Exception:
                        pass # Ignore errors for locked files

        return f"Cleaned {cleaned_files} old temporary files on Windows."

    elif platform.system() in ["Linux", "Darwin"]:
        # Basic temp cleanup
        temp_dirs = ['/tmp', '/var/tmp']
        cleaned_files = 0
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for item in os.listdir(temp_dir):
                    if item not in ['..', '.']:
                        full_path = os.path.join(temp_dir, item)
                        try:
                            # Use system command for robust removal (requires permissions)
                            subprocess.run(['rm', '-rf', full_path], check=True, capture_output=True)
                            cleaned_files += 1
                        except Exception:
                            pass
        return f"Attempted to clean {cleaned_files} items in /tmp and /var/tmp."
    
    return "System cleanup performed (basic)."

def get_battery_info():
    """Returns battery status if available (mainly for laptops)."""
    if not hasattr(psutil, 'sensors_battery') or psutil.sensors_battery() is None:
        return {"status": "N/A", "percent": "N/A", "time_left": "N/A", "plugged": False}
    
    battery = psutil.sensors_battery()
    
    if battery.power_plugged:
        status = "Charging"
    elif battery.percent == 100:
        status = "Full"
    elif battery.secsleft == psutil.POWER_TIME_UNLIMITED:
        status = "Discharging (Time not available)"
    else:
        status = "Discharging"
        
    time_left = "N/A"
    if battery.secsleft not in [psutil.POWER_TIME_UNLIMITED, psutil.POWER_TIME_UNKNOWN]:
        # Convert seconds to HH:MM format
        m, s = divmod(battery.secsleft, 60)
        h, m = divmod(m, 60)
        time_left = f"{h:d}h {m:02d}m"

    return {
        "status": status,
        "percent": battery.percent,
        "time_left": time_left,
        "plugged": battery.power_plugged
    }

def get_network_info():
    """Gets local network details (IP, gateway, Wi-Fi name)."""
    info = {"IP Address": "N/A", "Gateway": "N/A", "Wi-Fi Name": "N/A"}
    
    # 1. IP Address and Gateway (using psutil)
    stats = psutil.net_if_addrs()
    
    # Find active interface with an IPv4 address
    for name, addresses in stats.items():
        if name != 'lo': # Skip loopback
            for addr in addresses:
                if addr.family == 2: # AF_INET (IPv4)
                    info["IP Address"] = addr.address
                    
                    # Try to get Gateway using net_if_stats or routing table (complex, simplified here)
                    # This often requires running external commands, but we'll use a basic check
                    # Gateway detection is complex and platform-dependent, often requiring 'route' or 'ip route'.
                    # For simplicity, we skip gateway detection here to avoid external calls.
                    # info["Gateway"] is left as N/A
                    break
            
    # 2. Wi-Fi Name (SSID)
    if platform.system() == "Windows":
        try:
            # Requires running external command
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True, check=True)
            for line in result.stdout.split('\n'):
                if 'SSID' in line and ':' in line:
                    info["Wi-Fi Name"] = line.split(':')[-1].strip()
                    break
        except Exception:
            pass # Ignore errors if netsh fails
            
    elif platform.system() == "Darwin":
        try:
            # Requires running external command
            result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], capture_output=True, text=True, check=True)
            for line in result.stdout.split('\n'):
                if 'SSID' in line and ':' in line:
                    info["Wi-Fi Name"] = line.split(':')[-1].strip()
                    break
        except Exception:
            pass # Ignore errors

    return info

# --- FUN UTILITIES ---

def get_random_string(length=12):
    """Generates a simple random password-like string."""
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(length))

def get_fun_quote():
    """Fetches a random programming quote (using a public API)."""
    try:
        # Example API for programming quotes
        response = requests.get("https://programming-quotes-api.herokuapp.com/quotes/random/lang/en")
        data = response.json()
        return f"\"{data.get('en')}\" - {data.get('author')}"
    except Exception:
        return "Couldn't fetch an external quote. Enjoy coding!"

def get_fun_joke():
    """Provides programming-related jokes (Updated for English version)."""
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "Why do Java developers wear glasses? Because they can't C#!",
        "A SQL query goes into a bar, walks up to two tables and asks: 'Can I join you?'",
        "Why did the programmer quit his job? He didn't get arrays!",
        "What do you call a programmer from Finland? Nerdic.",
        "Why do Python programmers prefer snakes? Because they're always trying to catch exceptions!",
        "How do you comfort a JavaScript bug? You console it!",
        "Why don't programmers like nature? It has too many bugs.",
        "What's a programmer's favorite hangout place? The Foo Bar!"
    ]
    return random.choice(jokes)

# --- REMINDERS (requires plyer) ---
def set_reminder(title, message, delay_seconds):
    """Sets a desktop notification reminder after a delay."""
    # We delay the notification process to run after the bot command finishes.
    # Note: plyer requires a running application loop or threading to work correctly.
    # We will handle the threading aspect in commands.py
    from plyer import notification
    time.sleep(delay_seconds)
    notification.notify(
        title=title,
        message=message,
        app_name='Local Assistant Bot',
        timeout=10
    )
    return f"Reminder set for {delay_seconds} seconds."
