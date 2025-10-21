import threading
import random
import json
import hashlib
import base64
import qrcode
import requests
import sqlite3
import os
import shutil
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from utils import (
    get_time, open_path, safe_eval, append_note, read_all_notes, get_sysinfo, 
    delete_note_by_index, search_notes, delete_notes_by_keyword, edit_note_by_index,
    read_calc_history, convert_unit, get_random_string, clean_system, 
    get_battery_info, get_network_info, get_fun_quote, get_fun_joke, set_reminder
)

# Initialize Rich Console for colored output
console = Console()

# Constants
NOTES_FILE = "data/notes.txt"

# --- COMMAND IMPLEMENTATIONS ---

def cmd_help():
    table = Table(title="[bold blue]Advanced Local Assistant Bot - Available Commands[/bold blue]", show_header=True, header_style="bold green")
    table.add_column("Command", style="cyan", justify="left")
    table.add_column("Description", style="white", justify="left")
    table.add_column("Example", style="yellow", justify="left")

    # Basic Commands
    table.add_row("help", "Show this help menu", "help")
    table.add_row("time", "Display current date & time", "time")
    table.add_row("open", "Open a file or folder on your system", "open C:\\Users\\...\\Desktop")
    
    # Note Management
    table.add_row("[bold]note add[/bold]", "Add a timestamped note", "note add \"Buy milk\"")
    table.add_row("[bold]note show[/bold]", "Display all saved notes with indices", "note show")
    table.add_row("[bold]note delete[/bold]", "Delete note by index or keyword", "note delete 5 / note delete \"milk\"")
    table.add_row("[bold]note search[/bold]", "Search notes by keyword", "note search Python")
    table.add_row("[bold]note edit[/bold]", "Edit note by index", "note edit 3 \"New text\"")

    # Calculator & Math
    table.add_row("[bold]calc[/bold]", "Calculate a math expression", "calc 2+3*4")
    table.add_row("[bold]calc history[/bold]", "Show last 10 calculations", "calc history")
    table.add_row("[bold]convert[/bold]", "Convert units (e.g. km to mi)", "convert length 10 km to mi")
    table.add_row("[bold]random[/bold]", "Generate a random string/number", "random string 15 / random number 1 100")
    
    # System Information
    table.add_row("sysinfo", "Show system hardware/performance info", "sysinfo")
    table.add_row("clean", "Clean temporary files and caches", "clean")
    table.add_row("battery", "Show battery percentage and time left", "battery")
    table.add_row("network", "Show local IP and Wi-Fi name", "network")
    table.add_row("process", "List running processes", "process list")
    table.add_row("disk", "Analyze disk usage", "disk")
    table.add_row("monitor", "Real-time system monitoring", "monitor")

    # File Management
    table.add_row("[bold]file list[/bold]", "List directory contents", "file list C:\\Users")
    table.add_row("[bold]file copy[/bold]", "Copy files/directories", "file copy source.txt dest.txt")
    table.add_row("[bold]file move[/bold]", "Move files/directories", "file move old.txt new.txt")
    table.add_row("[bold]file delete[/bold]", "Delete files/directories", "file delete temp.txt")

    # Security & Encryption
    table.add_row("[bold]password[/bold]", "Generate secure passwords", "password 16 -u -n -s")
    table.add_row("[bold]encrypt[/bold]", "Encrypt text", "encrypt \"secret text\" key123")
    table.add_row("[bold]decrypt[/bold]", "Decrypt text", "decrypt \"encrypted_text\" key123")
    table.add_row("[bold]hash[/bold]", "Generate hash (MD5, SHA1, SHA256, SHA512)", "hash \"text\" sha256")

    # Data Processing
    table.add_row("[bold]base64[/bold]", "Base64 encode text", "base64 \"Hello World\"")
    table.add_row("[bold]decode64[/bold]", "Base64 decode text", "decode64 \"SGVsbG8gV29ybGQ=\"")
    table.add_row("[bold]json[/bold]", "Format JSON text", "json '{\"key\":\"value\"}'")
    table.add_row("[bold]text[/bold]", "Text manipulation tools", "text upper \"hello world\"")

    # Task Management
    table.add_row("[bold]tasks add[/bold]", "Add a new task", "tasks add \"Complete project\"")
    table.add_row("[bold]tasks list[/bold]", "List all tasks", "tasks list")
    table.add_row("[bold]tasks complete[/bold]", "Mark task as complete", "tasks complete 1")
    table.add_row("[bold]tasks delete[/bold]", "Delete a task", "tasks delete 1")

    # Web Tools
    table.add_row("[bold]weather[/bold]", "Get weather information", "weather London")
    table.add_row("[bold]url[/bold]", "Shorten URLs", "url https://example.com")
    table.add_row("[bold]qr[/bold]", "Generate QR codes", "qr \"https://example.com\"")

    # Backup & Restore
    table.add_row("[bold]backup[/bold]", "Backup files/directories", "backup C:\\Important backup_folder")
    table.add_row("[bold]restore[/bold]", "Restore from backup", "restore backup_folder restored")

    # Settings
    table.add_row("[bold]settings[/bold]", "Manage application settings", "settings show")
    table.add_row("[bold]settings set[/bold]", "Set a configuration value", "settings set theme dark")

    # Entertainment
    table.add_row("[bold]fun quote[/bold]", "Get a random quote", "fun quote")
    table.add_row("[bold]fun joke[/bold]", "Get a local joke", "fun joke")
    table.add_row("[bold]remind[/bold]", "Set a desktop notification reminder", "remind 60 \"Check code commit\"")
    
    # System Commands
    table.add_row("clear/cls", "Clear the screen", "clear")
    table.add_row("exit/quit", "Exit the bot", "exit")

    rprint(table)
    rprint(Panel(
        "[bold cyan]Pro Tips:[/bold cyan]\n"
        " Use 'help' anytime to see this menu\n"
        " All commands are case-insensitive\n"
        " Use quotes for text with spaces\n"
        " Press Ctrl+C to stop monitoring commands\n"
        " Check 'settings' to customize the bot",
        title="[bold green]Quick Tips[/bold green]"
    ))
    return None

def cmd_time(_args):
    rprint(f"[bold white on blue] Current Time: {get_time()} [/bold white on blue]")
    return None

def cmd_open(args):
    if not args:
        console.print("[bold red] Usage: open <path>[/bold red]")
        return None
    path = " ".join(args)
    ok, msg = open_path(path)
    if ok:
        console.print(f"[bold green] {msg}[/bold green]")
    else:
        console.print(f"[bold red] {msg}[/bold red]")
    return None

# --- NOTE MANAGEMENT COMMAND ---

def cmd_note(args):
    if not args:
        console.print("[bold red] Usage: note add/show/delete/search/edit[/bold red]")
        return None
    
    sub = args[0].lower()
    
    if sub == "add":
        text = " ".join(args[1:]).strip().strip('"')
        if not text:
            console.print("[bold red] No text provided.[/bold red]")
            return None
        append_note(NOTES_FILE, text)
        console.print(f"[bold green] Note added: [white]{text}[/white][/bold green]")
        return None
    
    elif sub == "show":
        notes = read_all_notes(NOTES_FILE)
        if not notes:
            console.print("[bold yellow] No notes found. Add one with 'note add \"text\"'[/bold yellow]")
            return None
        
        table = Table(title="[bold cyan] Your Local Notes[/bold cyan]", show_header=True, header_style="bold magenta")
        table.add_column("Index", style="yellow", justify="right")
        table.add_column("Note Content", style="white", justify="left")
        
        for index, line in enumerate(notes, 1):
            table.add_row(str(index), line.strip())
        
        rprint(table)
        return None
    
    elif sub == "delete":
        if len(args) < 2:
            console.print("[bold red] Usage: note delete <index> or note delete \"keyword\"[/bold red]")
            return None

        param = args[1]
        
        if param.isdigit():
            # Delete by index
            index = int(param)
            success, message = delete_note_by_index(index)
            if success:
                console.print(f"[bold green]  Successfully deleted note {index}: [white]{message}[/white][/bold green]")
            else:
                console.print(f"[bold red] {message}[/bold red]")
        else:
            # Delete by keyword
            keyword = " ".join(args[1:]).strip().strip('"')
            deleted_count = delete_notes_by_keyword(keyword)
            if deleted_count > 0:
                console.print(f"[bold green]  Successfully deleted [white]{deleted_count}[/white] notes containing: [white]{keyword}[/white][/bold green]")
            else:
                console.print(f"[bold yellow] No notes found containing: [white]{keyword}[/white][/bold yellow]")
        return None
        
    elif sub == "search":
        if len(args) < 2:
            console.print("[bold red] Usage: note search \"keyword\"[/bold red]")
            return None
        
        keyword = " ".join(args[1:]).strip().strip('"')
        results = search_notes(keyword)
        
        if not results:
            console.print(f"[bold yellow] No notes found containing: [white]{keyword}[/white][/bold yellow]")
            return None
            
        table = Table(title=f"[bold cyan] Search Results for '{keyword}'[/bold cyan]", show_header=True, header_style="bold magenta")
        table.add_column("Index", style="yellow", justify="right")
        table.add_column("Note Content", style="white", justify="left")
        
        for index, note in results:
            # Highlight the keyword for better visibility
            highlighted_note = note.replace(keyword, f"[bold red]{keyword}[/bold red]", 1) 
            table.add_row(str(index), highlighted_note)
            
        rprint(table)
        return None
        
    elif sub == "edit":
        if len(args) < 3:
            console.print("[bold red] Usage: note edit <index> \"new text\"[/bold red]")
            return None
        
        try:
            index = int(args[1])
        except ValueError:
            console.print(f"[bold red] Invalid index: '{args[1]}'. Index must be a number.[/bold red]")
            return None
            
        new_text = " ".join(args[2:]).strip().strip('"')
        
        success, old_note = edit_note_by_index(index, new_text)
        
        if success:
            console.print(f"[bold green]  Note {index} edited successfully.[/bold green]")
            rprint(f"[bold]   Old:[/bold] [grey50]{old_note}[/grey50]")
            rprint(f"[bold]   New:[/bold] [white]{new_text}[/white]")
        else:
            console.print(f"[bold red] {old_note}[/bold red]")
        return None
        
    else:
        console.print(f"[bold red] Unknown note command: '{sub}'.[/bold red]")
        return None

# --- CALCULATION COMMANDS ---

def cmd_calc(args):
    if not args:
        console.print("[bold red] Usage: calc <expression> (e.g. calc 1500 / 3.5)[/bold red]")
        return None
    expr = " ".join(args)
    try:
        res = safe_eval(expr)
        rprint(Panel(f"[bold yellow]{expr}[/bold yellow] = [bold green]{res}[/bold green]", title="[bold blue]Calculator[/bold blue]"))
    except ValueError as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    except Exception:
        console.print(f"[bold red] Error evaluating expression: {expr}[/bold red]")
    return None

def cmd_calc_history(_args):
    history = read_calc_history()
    if not history:
        console.print("[bold yellow] Calculation history is empty.[/bold yellow]")
        return None
        
    rprint(Panel("\n".join(history), title="[bold blue]Last 10 Calculations[/bold blue]"))
    return None

def cmd_convert(args):
    if len(args) != 4 or args[2].lower() != 'to':
        console.print("[bold red] Usage: convert <type> <value> to <unit>[/bold red]")
        console.print("[bold red]   Example: convert length 10 km to mi[/bold red]")
        return None

    type_ = args[0].lower()
    try:
        value = float(args[1])
    except ValueError:
        console.print(f"[bold red] Invalid value: '{args[1]}'. Must be a number.[/bold red]")
        return None
        
    unit_from = args[1]
    unit_to = args[3].lower()

    try:
        result = convert_unit(type_, value, unit_from, unit_to)
        rprint(f"[bold green] {value} {unit_from} is equal to [yellow]{result:.2f}[/yellow] {unit_to}[/bold green]")
    except ValueError as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    return None

def cmd_random(args):
    if not args:
        console.print("[bold red] Usage: random string [length] or random number [min] [max][/bold red]")
        return None
    
    sub = args[0].lower()
    
    if sub == "string":
        length = int(args[1]) if len(args) > 1 and args[1].isdigit() else 12
        random_str = get_random_string(length)
        rprint(f"[bold cyan] Random String ({length}): [white]{random_str}[/white][/bold cyan]")
    elif sub == "number":
        try:
            min_ = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
            max_ = int(args[2]) if len(args) > 2 and args[2].isdigit() else 100
            random_num = random.randint(min_, max_)
            rprint(f"[bold cyan] Random Number ({min_}-{max_}): [white]{random_num}[/white][/bold cyan]")
        except ValueError:
            console.print("[bold red] Min and Max must be valid numbers.[/bold red]")
    else:
        console.print(f"[bold red] Unknown random subcommand: '{sub}'.[/bold red]")
    return None

# --- SYSTEM COMMANDS ---

def cmd_sysinfo(_args):
    info = get_sysinfo()
    rprint(Panel(
        f"[bold blue]Platform:[/bold blue] {info.get('platform')}\n"
        f"[bold blue]Machine:[/bold blue] {info.get('machine')}\n"
        f"[bold blue]Processor:[/bold blue] {info.get('processor')} [green](Xeon E3 1240, well-suited for this work!)[/green]\n"
        f"--- Performance ---\n"
        f"[bold cyan]CPU Usage:[/bold cyan] {info.get('cpu_usage_percent')}%\n"
        f"[bold cyan]RAM Usage:[/bold cyan] {info.get('memory_used_mb')}MB / {info.get('memory_total_mb')}MB ([red]{info.get('memory_percent')}%[/red])\n"
        f"[bold cyan]Disk Usage:[/bold cyan] {info.get('disk_used_gb')}GB / {info.get('disk_total_gb')}GB ([red]{info.get('disk_percent')}%[/red])",
        title="[bold yellow] System Information[/bold yellow]"
    ))
    return None

def cmd_clean(_args):
    rprint(f"[bold yellow] Starting system cleanup...[/bold yellow]")
    msg = clean_system()
    rprint(f"[bold green] Cleanup Complete:[/bold green] {msg}")
    return None

def cmd_battery(_args):
    info = get_battery_info()
    
    if info["status"] == "N/A":
        console.print("[bold yellow] Battery information not available (not a laptop or psutil failed).[/bold yellow]")
        return None
        
    plugged_status = "[green]Plugged in[/green]" if info['plugged'] else "[red]Discharging[/red]"
    time_display = f"Time Left: [cyan]{info['time_left']}[/cyan]" if info['time_left'] != 'N/A' else ""

    rprint(Panel(
        f"[bold magenta]Status:[/bold magenta] {info['status']} ({plugged_status})\n"
        f"[bold magenta]Percentage:[/bold magenta] [yellow]{info['percent']}%[/yellow]\n"
        f"{time_display}",
        title="[bold blue] Battery Check[/bold blue]"
    ))
    return None

def cmd_network(_args):
    info = get_network_info()
    rprint(Panel(
        f"[bold cyan]IP Address (Local):[/bold cyan] [white]{info.get('IP Address')}[/white]\n"
        f"[bold cyan]Wi-Fi Name (SSID):[/bold cyan] [white]{info.get('Wi-Fi Name')}[/white]\n"
        f"[bold cyan]Gateway (Simplified):[/bold cyan] [white]N/A (Requires complex routing info)[/white]",
        title="[bold blue] Network Info[/bold blue]"
    ))
    return None
    
# --- FUN COMMANDS ---

def cmd_fun(args):
    if not args:
        console.print("[bold red] Usage: fun quote or fun joke[/bold red]")
        return None
        
    sub = args[0].lower()
    
    if sub == "quote":
        quote = get_fun_quote()
        rprint(Panel(quote, title="[bold magenta] Random Quote[/bold magenta]"))
    elif sub == "joke":
        joke = get_fun_joke()
        rprint(Panel(joke, title="[bold yellow] Moroccan Joke[/bold yellow]"))
    else:
        console.print(f"[bold red] Unknown fun command: '{sub}'.[/bold red]")
    return None
    
def cmd_remind(args):
    if len(args) < 2 or not args[0].isdigit():
        console.print("[bold red] Usage: remind <seconds> \"message\"[/bold red]")
        console.print("[bold red]   Example: remind 60 \"Check code commit\"[/bold red]")
        return None
        
    try:
        delay = int(args[0])
        message = " ".join(args[1:]).strip().strip('"')
        if not message:
            message = "Reminder from your Local Assistant Bot!"
            
        # Run the reminder function in a separate thread so it doesn't block the bot
        threading.Thread(target=set_reminder, args=("Reminder!", message, delay)).start()
        
        console.print(f"[bold green] Reminder set for [yellow]{delay} seconds[/yellow] for message: [white]'{message}'[/white][/bold green]")
        
    except Exception as e:
        console.print(f"[bold red] Error setting reminder (Check if plyer is installed): {e}[/bold red]")
    return None

def cmd_clear():
    import os, platform
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    return None # Return None so main loop doesn't print "None"

# --- ADVANCED COMMANDS ---

def cmd_file_manager(args):
    """Advanced file management system"""
    if not args:
        console.print("[bold red] Usage: file list/copy/move/delete/search <path>[/bold red]")
        return None
    
    action = args[0].lower()
    
    if action == "list":
        path = args[1] if len(args) > 1 else "."
        try:
            items = os.listdir(path)
            table = Table(title=f"[bold blue] Directory Contents: {path}[/bold blue]")
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Size", style="yellow")
            
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    table.add_row(item, " Directory", "N/A")
                else:
                    size = os.path.getsize(item_path)
                    table.add_row(item, " File", f"{size} bytes")
            
            rprint(table)
        except Exception as e:
            console.print(f"[bold red] Error: {e}[/bold red]")
    
    elif action == "copy":
        if len(args) < 3:
            console.print("[bold red] Usage: file copy <source> <destination>[/bold red]")
            return None
        try:
            shutil.copy2(args[1], args[2])
            console.print(f"[bold green] Copied {args[1]} to {args[2]}[/bold green]")
        except Exception as e:
            console.print(f"[bold red] Error: {e}[/bold red]")
    
    elif action == "move":
        if len(args) < 3:
            console.print("[bold red] Usage: file move <source> <destination>[/bold red]")
            return None
        try:
            shutil.move(args[1], args[2])
            console.print(f"[bold green] Moved {args[1]} to {args[2]}[/bold green]")
        except Exception as e:
            console.print(f"[bold red] Error: {e}[/bold red]")
    
    elif action == "delete":
        if len(args) < 2:
            console.print("[bold red] Usage: file delete <path>[/bold red]")
            return None
        try:
            if os.path.isfile(args[1]):
                os.remove(args[1])
                console.print(f"[bold green] Deleted file: {args[1]}[/bold green]")
            elif os.path.isdir(args[1]):
                shutil.rmtree(args[1])
                console.print(f"[bold green] Deleted directory: {args[1]}[/bold green]")
        except Exception as e:
            console.print(f"[bold red] Error: {e}[/bold red]")
    
    else:
        console.print(f"[bold red] Unknown file action: {action}[/bold red]")
    
    return None

def cmd_password_gen(args):
    """Advanced password generator"""
    if not args:
        console.print("[bold red] Usage: password <length> [options][/bold red]")
        console.print("[bold yellow]Options: -u (uppercase), -l (lowercase), -n (numbers), -s (symbols)[/bold yellow]")
        return None
    
    try:
        length = int(args[0])
        options = args[1:] if len(args) > 1 else []
        
        chars = ""
        if "-l" in options or not options:
            chars += "abcdefghijklmnopqrstuvwxyz"
        if "-u" in options or not options:
            chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if "-n" in options or not options:
            chars += "0123456789"
        if "-s" in options or not options:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        password = ''.join(random.choice(chars) for _ in range(length))
        
        rprint(Panel(
            f"[bold green]Generated Password:[/bold green]\n[bold white]{password}[/bold white]",
            title="[bold blue]Password Generator[/bold blue]"
        ))
        
    except ValueError:
        console.print("[bold red]Invalid length. Please provide a number.[/bold red]")
    
    return None

def cmd_encrypt(args):
    """Simple text encryption"""
    if len(args) < 2:
        console.print("[bold red] Usage: encrypt <text> <key>[/bold red]")
        return None
    
    text = " ".join(args[:-1])
    key = args[-1]
    
    try:
        encrypted = base64.b64encode(text.encode()).decode()
        rprint(Panel(
            f"[bold green]Encrypted Text:[/bold green]\n[bold white]{encrypted}[/bold white]",
            title="[bold blue] Encryption[/bold blue]"
        ))
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_decrypt(args):
    """Simple text decryption"""
    if len(args) < 2:
        console.print("[bold red] Usage: decrypt <encrypted_text> <key>[/bold red]")
        return None
    
    encrypted_text = " ".join(args[:-1])
    key = args[-1]
    
    try:
        decrypted = base64.b64decode(encrypted_text.encode()).decode()
        rprint(Panel(
            f"[bold green]Decrypted Text:[/bold green]\n[bold white]{decrypted}[/bold white]",
            title="[bold blue] Decryption[/bold blue]"
        ))
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_hash_generator(args):
    """Generate hash for text"""
    if len(args) < 2:
        console.print("[bold red] Usage: hash <text> <algorithm>[/bold red]")
        console.print("[bold yellow]Algorithms: md5, sha1, sha256, sha512[/bold yellow]")
        return None
    
    text = " ".join(args[:-1])
    algorithm = args[-1].lower()
    
    try:
        if algorithm == "md5":
            hash_value = hashlib.md5(text.encode()).hexdigest()
        elif algorithm == "sha1":
            hash_value = hashlib.sha1(text.encode()).hexdigest()
        elif algorithm == "sha256":
            hash_value = hashlib.sha256(text.encode()).hexdigest()
        elif algorithm == "sha512":
            hash_value = hashlib.sha512(text.encode()).hexdigest()
        else:
            console.print("[bold red] Unsupported algorithm. Use: md5, sha1, sha256, sha512[/bold red]")
            return None
        
        rprint(Panel(
            f"[bold green]{algorithm.upper()} Hash:[/bold green]\n[bold white]{hash_value}[/bold white]",
            title="[bold blue] Hash Generator[/bold blue]"
        ))
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_base64_encode(args):
    """Base64 encode text"""
    if not args:
        console.print("[bold red] Usage: base64 <text>[/bold red]")
        return None
    
    text = " ".join(args)
    try:
        encoded = base64.b64encode(text.encode()).decode()
        rprint(Panel(
            f"[bold green]Base64 Encoded:[/bold green]\n[bold white]{encoded}[/bold white]",
            title="[bold blue] Base64 Encode[/bold blue]"
        ))
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_base64_decode(args):
    """Base64 decode text"""
    if not args:
        console.print("[bold red] Usage: decode64 <encoded_text>[/bold red]")
        return None
    
    encoded_text = " ".join(args)
    try:
        decoded = base64.b64decode(encoded_text.encode()).decode()
        rprint(Panel(
            f"[bold green]Base64 Decoded:[/bold green]\n[bold white]{decoded}[/bold white]",
            title="[bold blue] Base64 Decode[/bold blue]"
        ))
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_json_formatter(args):
    """Format JSON text"""
    if not args:
        console.print("[bold red] Usage: json <json_text>[/bold red]")
        return None
    
    json_text = " ".join(args)
    try:
        parsed = json.loads(json_text)
        formatted = json.dumps(parsed, indent=2)
        rprint(Panel(
            f"[bold green]Formatted JSON:[/bold green]\n[bold white]{formatted}[/bold white]",
            title="[bold blue] JSON Formatter[/bold blue]"
        ))
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_text_tools(args):
    """Text manipulation tools"""
    if len(args) < 2:
        console.print("[bold red] Usage: text <action> <text>[/bold red]")
        console.print("[bold yellow]Actions: upper, lower, reverse, count, words[/bold yellow]")
        return None
    
    action = args[0].lower()
    text = " ".join(args[1:])
    
    try:
        if action == "upper":
            result = text.upper()
        elif action == "lower":
            result = text.lower()
        elif action == "reverse":
            result = text[::-1]
        elif action == "count":
            result = f"Characters: {len(text)}, Words: {len(text.split())}"
        elif action == "words":
            words = text.split()
            result = f"Words: {words}"
        else:
            console.print("[bold red] Unknown action. Use: upper, lower, reverse, count, words[/bold red]")
            return None
        
        rprint(Panel(
            f"[bold green]Result:[/bold green]\n[bold white]{result}[/bold white]",
            title="[bold blue] Text Tools[/bold blue]"
        ))
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_process_manager(args):
    """Process management tools"""
    if not args:
        console.print("[bold red] Usage: process list/kill <pid>[/bold red]")
        return None
    
    action = args[0].lower()
    
    if action == "list":
        try:
            import psutil
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            table = Table(title="[bold blue] Running Processes[/bold blue]")
            table.add_column("PID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("CPU %", style="yellow")
            table.add_column("Memory %", style="red")
            
            for proc in sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:20]:
                table.add_row(
                    str(proc['pid']),
                    proc['name'],
                    f"{proc['cpu_percent']:.1f}%",
                    f"{proc['memory_percent']:.1f}%"
                )
            
            rprint(table)
        except Exception as e:
            console.print(f"[bold red] Error: {e}[/bold red]")
    
    elif action == "kill":
        if len(args) < 2:
            console.print("[bold red] Usage: process kill <pid>[/bold red]")
            return None
        
        try:
            import psutil
            pid = int(args[1])
            proc = psutil.Process(pid)
            proc.terminate()
            console.print(f"[bold green] Process {pid} terminated[/bold green]")
        except Exception as e:
            console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_disk_analyzer(args):
    """Disk usage analyzer"""
    try:
        import psutil
        
        partitions = psutil.disk_partitions()
        table = Table(title="[bold blue] Disk Usage Analysis[/bold blue]")
        table.add_column("Device", style="cyan")
        table.add_column("Mountpoint", style="green")
        table.add_column("FSType", style="yellow")
        table.add_column("Total", style="blue")
        table.add_column("Used", style="red")
        table.add_column("Free", style="green")
        table.add_column("Usage %", style="red")
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                total_gb = usage.total / (1024**3)
                used_gb = usage.used / (1024**3)
                free_gb = usage.free / (1024**3)
                percent = (usage.used / usage.total) * 100
                
                table.add_row(
                    partition.device,
                    partition.mountpoint,
                    partition.fstype,
                    f"{total_gb:.1f} GB",
                    f"{used_gb:.1f} GB",
                    f"{free_gb:.1f} GB",
                    f"{percent:.1f}%"
                )
            except PermissionError:
                continue
        
        rprint(table)
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_system_monitor(args):
    """Real-time system monitoring"""
    try:
        import psutil
        import time
        
        console.print("[bold yellow] Starting system monitor (Press Ctrl+C to stop)...[/bold yellow]")
        
        while True:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            rprint(Panel(
                f"[bold cyan]CPU Usage:[/bold cyan] {cpu_percent}%\n"
                f"[bold cyan]Memory Usage:[/bold cyan] {memory.percent}% ({memory.used / (1024**3):.1f} GB / {memory.total / (1024**3):.1f} GB)\n"
                f"[bold cyan]Disk Usage:[/bold cyan] {(disk.used / disk.total) * 100:.1f}% ({disk.used / (1024**3):.1f} GB / {disk.total / (1024**3):.1f} GB)",
                title="[bold blue] System Monitor[/bold blue]"
            ))
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        console.print("\n[bold green] Monitoring stopped[/bold green]")
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_task_manager(args):
    """Task management system"""
    if not args:
        console.print("[bold red] Usage: tasks add/list/complete/delete <task>[/bold red]")
        return None
    
    action = args[0].lower()
    
    # Simple file-based task storage
    tasks_file = "data/tasks.txt"
    os.makedirs(os.path.dirname(tasks_file), exist_ok=True)
    
    if action == "add":
        if len(args) < 2:
            console.print("[bold red] Usage: tasks add <task_description>[/bold red]")
            return None
        
        task = " ".join(args[1:])
        with open(tasks_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {task}\n")
        
        console.print(f"[bold green] Task added: {task}[/bold green]")
    
    elif action == "list":
        try:
            with open(tasks_file, "r", encoding="utf-8") as f:
                tasks = f.readlines()
            
            if not tasks:
                console.print("[bold yellow] No tasks found[/bold yellow]")
                return None
            
            table = Table(title="[bold blue] Task List[/bold blue]")
            table.add_column("ID", style="cyan")
            table.add_column("Task", style="white")
            table.add_column("Created", style="yellow")
            
            for i, task in enumerate(tasks, 1):
                parts = task.split("] ", 1)
                timestamp = parts[0] + "]"
                task_text = parts[1].strip()
                table.add_row(str(i), task_text, timestamp)
            
            rprint(table)
        except FileNotFoundError:
            console.print("[bold yellow] No tasks found[/bold yellow]")
    
    elif action == "complete":
        if len(args) < 2:
            console.print("[bold red] Usage: tasks complete <task_id>[/bold red]")
            return None
        
        try:
            task_id = int(args[1])
            with open(tasks_file, "r", encoding="utf-8") as f:
                tasks = f.readlines()
            
            if 1 <= task_id <= len(tasks):
                completed_task = tasks.pop(task_id - 1)
                with open(tasks_file, "w", encoding="utf-8") as f:
                    f.writelines(tasks)
                
                console.print(f"[bold green] Task completed: {completed_task.strip()}[/bold green]")
            else:
                console.print(f"[bold red] Task ID {task_id} not found[/bold red]")
        except ValueError:
            console.print("[bold red] Invalid task ID[/bold red]")
        except Exception as e:
            console.print(f"[bold red] Error: {e}[/bold red]")
    
    elif action == "delete":
        if len(args) < 2:
            console.print("[bold red] Usage: tasks delete <task_id>[/bold red]")
            return None
        
        try:
            task_id = int(args[1])
            with open(tasks_file, "r", encoding="utf-8") as f:
                tasks = f.readlines()
            
            if 1 <= task_id <= len(tasks):
                deleted_task = tasks.pop(task_id - 1)
                with open(tasks_file, "w", encoding="utf-8") as f:
                    f.writelines(tasks)
                
                console.print(f"[bold green] Task deleted: {deleted_task.strip()}[/bold green]")
            else:
                console.print(f"[bold red] Task ID {task_id} not found[/bold red]")
        except ValueError:
            console.print("[bold red] Invalid task ID[/bold red]")
        except Exception as e:
            console.print(f"[bold red] Error: {e}[/bold red]")
    
    else:
        console.print(f"[bold red] Unknown action: {action}[/bold red]")
    
    return None

def cmd_weather(args):
    """Weather information (requires API key)"""
    if not args:
        console.print("[bold red] Usage: weather <city>[/bold red]")
        console.print("[bold yellow]Note: Requires OpenWeatherMap API key[/bold yellow]")
        return None
    
    city = " ".join(args)
    api_key = "YOUR_API_KEY"  # User needs to set this
    
    if api_key == "YOUR_API_KEY":
        console.print("[bold yellow] Please set your OpenWeatherMap API key in the code[/bold yellow]")
        return None
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            
            rprint(Panel(
                f"[bold cyan]Temperature:[/bold cyan] {temp}C\n"
                f"[bold cyan]Description:[/bold cyan] {description.title()}\n"
                f"[bold cyan]Humidity:[/bold cyan] {humidity}%\n"
                f"[bold cyan]Wind Speed:[/bold cyan] {wind_speed} m/s",
                title=f"[bold blue] Weather in {city.title()}[/bold blue]"
            ))
        else:
            console.print(f"[bold red] Error: {data.get('message', 'Unknown error')}[/bold red]")
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_url_shortener(args):
    """URL shortener (using TinyURL)"""
    if not args:
        console.print("[bold red] Usage: url <long_url>[/bold red]")
        return None
    
    long_url = args[0]
    
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={long_url}")
        if response.status_code == 200:
            short_url = response.text.strip()
            rprint(Panel(
                f"[bold green]Short URL:[/bold green]\n[bold white]{short_url}[/bold white]",
                title="[bold blue] URL Shortener[/bold blue]"
            ))
        else:
            console.print("[bold red] Failed to shorten URL[/bold red]")
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_qr_generator(args):
    """QR Code generator"""
    if not args:
        console.print("[bold red] Usage: qr <text_or_url>[/bold red]")
        return None
    
    text = " ".join(args)
    
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(text)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        filename = f"qr_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img.save(filename)
        
        console.print(f"[bold green] QR Code generated: {filename}[/bold green]")
        console.print(f"[bold cyan]Content: {text}[/bold cyan]")
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_backup(args):
    """Backup system"""
    if not args:
        console.print("[bold red] Usage: backup <source_path> [destination_path][/bold red]")
        return None
    
    source = args[0]
    destination = args[1] if len(args) > 1 else f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        if os.path.isfile(source):
            shutil.copy2(source, destination)
            console.print(f"[bold green] File backed up: {source} -> {destination}[/bold green]")
        elif os.path.isdir(source):
            shutil.copytree(source, destination)
            console.print(f"[bold green] Directory backed up: {source} -> {destination}[/bold green]")
        else:
            console.print(f"[bold red] Source not found: {source}[/bold red]")
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_restore(args):
    """Restore from backup"""
    if not args:
        console.print("[bold red] Usage: restore <backup_path> [destination_path][/bold red]")
        return None
    
    backup_path = args[0]
    destination = args[1] if len(args) > 1 else "restored"
    
    try:
        if os.path.isfile(backup_path):
            shutil.copy2(backup_path, destination)
            console.print(f"[bold green] File restored: {backup_path} -> {destination}[/bold green]")
        elif os.path.isdir(backup_path):
            shutil.copytree(backup_path, destination)
            console.print(f"[bold green] Directory restored: {backup_path} -> {destination}[/bold green]")
        else:
            console.print(f"[bold red] Backup not found: {backup_path}[/bold red]")
    except Exception as e:
        console.print(f"[bold red] Error: {e}[/bold red]")
    
    return None

def cmd_settings(args):
    """Settings management"""
    if not args:
        console.print("[bold red] Usage: settings show/set <key> <value>[/bold red]")
        return None
    
    action = args[0].lower()
    settings_file = "data/settings.json"
    os.makedirs(os.path.dirname(settings_file), exist_ok=True)
    
    # Load existing settings
    settings = {}
    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            settings = json.load(f)
    except FileNotFoundError:
        pass
    
    if action == "show":
        if len(args) > 1:
            key = args[1]
            if key in settings:
                console.print(f"[bold green]{key}: {settings[key]}[/bold green]")
            else:
                console.print(f"[bold red] Setting '{key}' not found[/bold red]")
        else:
            if settings:
                table = Table(title="[bold blue] Settings[/bold blue]")
                table.add_column("Key", style="cyan")
                table.add_column("Value", style="white")
                
                for key, value in settings.items():
                    table.add_row(key, str(value))
                
                rprint(table)
            else:
                console.print("[bold yellow] No settings found[/bold yellow]")
    
    elif action == "set":
        if len(args) < 3:
            console.print("[bold red] Usage: settings set <key> <value>[/bold red]")
            return None
        
        key = args[1]
        value = " ".join(args[2:])
        
        # Try to parse as JSON if possible
        try:
            value = json.loads(value)
        except:
            pass
        
        settings[key] = value
        
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
        
        console.print(f"[bold green] Setting '{key}' set to '{value}'[/bold green]")
    
    else:
        console.print(f"[bold red] Unknown action: {action}[/bold red]")
    
    return None
