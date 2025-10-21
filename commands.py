import threading
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

# --- COMMAND IMPLEMENTATIONS ---

def cmd_help():
    table = Table(title="[bold blue]Available Commands[/bold blue]", show_header=True, header_style="bold green")
    table.add_column("Command", style="cyan", justify="left")
    table.add_column("Description", style="white", justify="left")
    table.add_column("Example", style="yellow", justify="left")

    table.add_row("help", "Show this help menu", "help")
    table.add_row("time", "Display current date & time", "time")
    table.add_row("open", "Open a file or folder on your system", "open C:\\Users\\...\\Desktop")
    
    table.add_row("[bold]note add[/bold]", "Add a timestamped note", "note add \"Buy milk\"")
    table.add_row("[bold]note show[/bold]", "Display all saved notes with indices", "note show")
    table.add_row("[bold]note delete[/bold]", "Delete note by index or keyword", "note delete 5 / note delete \"milk\"")
    table.add_row("[bold]note search[/bold]", "Search notes by keyword", "note search Python")
    table.add_row("[bold]note edit[/bold]", "Edit note by index", "note edit 3 \"New text\"")

    table.add_row("[bold]calc[/bold]", "Calculate a math expression", "calc 2+3*4")
    table.add_row("[bold]calc history[/bold]", "Show last 10 calculations", "calc history")
    table.add_row("[bold]convert[/bold]", "Convert units (e.g. km to mi)", "convert length 10 km to mi")
    table.add_row("[bold]random[/bold]", "Generate a random string/number", "random string 15 / random number 1 100")
    
    table.add_row("sysinfo", "Show system hardware/performance info", "sysinfo")
    table.add_row("clean", "Clean temporary files and caches", "clean")
    table.add_row("battery", "Show battery percentage and time left", "battery")
    table.add_row("network", "Show local IP and Wi-Fi name", "network")

    table.add_row("[bold]fun quote[/bold]", "Get a random quote", "fun quote")
    table.add_row("[bold]fun joke[/bold]", "Get a local joke", "fun joke")
    table.add_row("[bold]remind[/bold]", "Set a desktop notification reminder", "remind 60 \"Check code commit\"")
    
    table.add_row("clear/cls", "Clear the screen", "clear")
    table.add_row("exit/quit", "Exit the bot", "exit")

    rprint(table)
    return None

def cmd_time(_args):
    rprint(f"[bold white on blue] ⏰ Current Time: {get_time()} [/bold white on blue]")
    return None

def cmd_open(args):
    if not args:
        console.print("[bold red]❌ Usage: open <path>[/bold red]")
        return None
    path = " ".join(args)
    ok, msg = open_path(path)
    if ok:
        console.print(f"[bold green]✅ {msg}[/bold green]")
    else:
        console.print(f"[bold red]❌ {msg}[/bold red]")
    return None

# --- NOTE MANAGEMENT COMMAND ---

def cmd_note(args):
    if not args:
        console.print("[bold red]❌ Usage: note add/show/delete/search/edit[/bold red]")
        return None
    
    sub = args[0].lower()
    
    if sub == "add":
        text = " ".join(args[1:]).strip().strip('"')
        if not text:
            console.print("[bold red]❌ No text provided.[/bold red]")
            return None
        append_note(NOTES_FILE, text)
        console.print(f"[bold green]✅ Note added: [white]{text}[/white][/bold green]")
        return None
    
    elif sub == "show":
        notes = read_all_notes(NOTES_FILE)
        if not notes:
            console.print("[bold yellow]💡 No notes found. Add one with 'note add \"text\"'[/bold yellow]")
            return None
        
        table = Table(title="[bold cyan]📝 Your Local Notes[/bold cyan]", show_header=True, header_style="bold magenta")
        table.add_column("Index", style="yellow", justify="right")
        table.add_column("Note Content", style="white", justify="left")
        
        for index, line in enumerate(notes, 1):
            table.add_row(str(index), line.strip())
        
        rprint(table)
        return None
    
    elif sub == "delete":
        if len(args) < 2:
            console.print("[bold red]❌ Usage: note delete <index> or note delete \"keyword\"[/bold red]")
            return None

        param = args[1]
        
        if param.isdigit():
            # Delete by index
            index = int(param)
            success, message = delete_note_by_index(index)
            if success:
                console.print(f"[bold green]🗑️  Successfully deleted note {index}: [white]{message}[/white][/bold green]")
            else:
                console.print(f"[bold red]❌ {message}[/bold red]")
        else:
            # Delete by keyword
            keyword = " ".join(args[1:]).strip().strip('"')
            deleted_count = delete_notes_by_keyword(keyword)
            if deleted_count > 0:
                console.print(f"[bold green]🗑️  Successfully deleted [white]{deleted_count}[/white] notes containing: [white]{keyword}[/white][/bold green]")
            else:
                console.print(f"[bold yellow]💡 No notes found containing: [white]{keyword}[/white][/bold yellow]")
        return None
        
    elif sub == "search":
        if len(args) < 2:
            console.print("[bold red]❌ Usage: note search \"keyword\"[/bold red]")
            return None
        
        keyword = " ".join(args[1:]).strip().strip('"')
        results = search_notes(keyword)
        
        if not results:
            console.print(f"[bold yellow]💡 No notes found containing: [white]{keyword}[/white][/bold yellow]")
            return None
            
        table = Table(title=f"[bold cyan]🔍 Search Results for '{keyword}'[/bold cyan]", show_header=True, header_style="bold magenta")
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
            console.print("[bold red]❌ Usage: note edit <index> \"new text\"[/bold red]")
            return None
        
        try:
            index = int(args[1])
        except ValueError:
            console.print(f"[bold red]❌ Invalid index: '{args[1]}'. Index must be a number.[/bold red]")
            return None
            
        new_text = " ".join(args[2:]).strip().strip('"')
        
        success, old_note = edit_note_by_index(index, new_text)
        
        if success:
            console.print(f"[bold green]✍️  Note {index} edited successfully.[/bold green]")
            rprint(f"[bold]   Old:[/bold] [grey50]{old_note}[/grey50]")
            rprint(f"[bold]   New:[/bold] [white]{new_text}[/white]")
        else:
            console.print(f"[bold red]❌ {old_note}[/bold red]")
        return None
        
    else:
        console.print(f"[bold red]❌ Unknown note command: '{sub}'.[/bold red]")
        return None

# --- CALCULATION COMMANDS ---

def cmd_calc(args):
    if not args:
        console.print("[bold red]❌ Usage: calc <expression> (e.g. calc 1500 / 3.5)[/bold red]")
        return None
    expr = " ".join(args)
    try:
        res = safe_eval(expr)
        rprint(Panel(f"[bold yellow]{expr}[/bold yellow] = [bold green]{res}[/bold green]", title="[bold blue]Calculator[/bold blue]"))
    except ValueError as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
    except Exception:
        console.print(f"[bold red]❌ Error evaluating expression: {expr}[/bold red]")
    return None

def cmd_calc_history(_args):
    history = read_calc_history()
    if not history:
        console.print("[bold yellow]💡 Calculation history is empty.[/bold yellow]")
        return None
        
    rprint(Panel("\n".join(history), title="[bold blue]Last 10 Calculations[/bold blue]"))
    return None

def cmd_convert(args):
    if len(args) != 4 or args[2].lower() != 'to':
        console.print("[bold red]❌ Usage: convert <type> <value> to <unit>[/bold red]")
        console.print("[bold red]   Example: convert length 10 km to mi[/bold red]")
        return None

    type_ = args[0].lower()
    try:
        value = float(args[1])
    except ValueError:
        console.print(f"[bold red]❌ Invalid value: '{args[1]}'. Must be a number.[/bold red]")
        return None
        
    unit_from = args[1]
    unit_to = args[3].lower()

    try:
        result = convert_unit(type_, value, unit_from, unit_to)
        rprint(f"[bold green]✅ {value} {unit_from} is equal to [yellow]{result:.2f}[/yellow] {unit_to}[/bold green]")
    except ValueError as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
    return None

def cmd_random(args):
    if not args:
        console.print("[bold red]❌ Usage: random string [length] or random number [min] [max][/bold red]")
        return None
    
    sub = args[0].lower()
    
    if sub == "string":
        length = int(args[1]) if len(args) > 1 and args[1].isdigit() else 12
        random_str = get_random_string(length)
        rprint(f"[bold cyan]🔐 Random String ({length}): [white]{random_str}[/white][/bold cyan]")
    elif sub == "number":
        try:
            min_ = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
            max_ = int(args[2]) if len(args) > 2 and args[2].isdigit() else 100
            random_num = random.randint(min_, max_)
            rprint(f"[bold cyan]🔢 Random Number ({min_}-{max_}): [white]{random_num}[/white][/bold cyan]")
        except ValueError:
            console.print("[bold red]❌ Min and Max must be valid numbers.[/bold red]")
    else:
        console.print(f"[bold red]❌ Unknown random subcommand: '{sub}'.[/bold red]")
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
        title="[bold yellow]🤖 System Information[/bold yellow]"
    ))
    return None

def cmd_clean(_args):
    rprint(f"[bold yellow]⏳ Starting system cleanup...[/bold yellow]")
    msg = clean_system()
    rprint(f"[bold green]✅ Cleanup Complete:[/bold green] {msg}")
    return None

def cmd_battery(_args):
    info = get_battery_info()
    
    if info["status"] == "N/A":
        console.print("[bold yellow]💡 Battery information not available (not a laptop or psutil failed).[/bold yellow]")
        return None
        
    plugged_status = "[green]Plugged in[/green]" if info['plugged'] else "[red]Discharging[/red]"
    time_display = f"Time Left: [cyan]{info['time_left']}[/cyan]" if info['time_left'] != 'N/A' else ""

    rprint(Panel(
        f"[bold magenta]Status:[/bold magenta] {info['status']} ({plugged_status})\n"
        f"[bold magenta]Percentage:[/bold magenta] [yellow]{info['percent']}%[/yellow]\n"
        f"{time_display}",
        title="[bold blue]🔋 Battery Check[/bold blue]"
    ))
    return None

def cmd_network(_args):
    info = get_network_info()
    rprint(Panel(
        f"[bold cyan]IP Address (Local):[/bold cyan] [white]{info.get('IP Address')}[/white]\n"
        f"[bold cyan]Wi-Fi Name (SSID):[/bold cyan] [white]{info.get('Wi-Fi Name')}[/white]\n"
        f"[bold cyan]Gateway (Simplified):[/bold cyan] [white]N/A (Requires complex routing info)[/white]",
        title="[bold blue]📡 Network Info[/bold blue]"
    ))
    return None
    
# --- FUN COMMANDS ---

def cmd_fun(args):
    if not args:
        console.print("[bold red]❌ Usage: fun quote or fun joke[/bold red]")
        return None
        
    sub = args[0].lower()
    
    if sub == "quote":
        quote = get_fun_quote()
        rprint(Panel(quote, title="[bold magenta]✨ Random Quote[/bold magenta]"))
    elif sub == "joke":
        joke = get_fun_joke()
        rprint(Panel(joke, title="[bold yellow]😂 Moroccan Joke[/bold yellow]"))
    else:
        console.print(f"[bold red]❌ Unknown fun command: '{sub}'.[/bold red]")
    return None
    
def cmd_remind(args):
    if len(args) < 2 or not args[0].isdigit():
        console.print("[bold red]❌ Usage: remind <seconds> \"message\"[/bold red]")
        console.print("[bold red]   Example: remind 60 \"Check code commit\"[/bold red]")
        return None
        
    try:
        delay = int(args[0])
        message = " ".join(args[1:]).strip().strip('"')
        if not message:
            message = "Reminder from your Local Assistant Bot!"
            
        # Run the reminder function in a separate thread so it doesn't block the bot
        threading.Thread(target=set_reminder, args=("Reminder!", message, delay)).start()
        
        console.print(f"[bold green]🔔 Reminder set for [yellow]{delay} seconds[/yellow] for message: [white]'{message}'[/white][/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Error setting reminder (Check if plyer is installed): {e}[/bold red]")
    return None

def cmd_clear():
    import os, platform
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    return None # Return None so main loop doesn't print "None"
