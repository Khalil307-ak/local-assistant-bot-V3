import shlex
import os
from rich.console import Console
from rich import print as rprint
from commands import (
    cmd_help, cmd_time, cmd_open, cmd_note, cmd_calc, cmd_sysinfo, cmd_clear,
    cmd_calc_history, cmd_convert, cmd_random, cmd_clean, cmd_battery, 
    cmd_network, cmd_fun, cmd_remind
)

console = Console()

# --- COMMAND MAP ---
COMMAND_MAP = {
    "help": lambda args: cmd_help(),
    "time": lambda args: cmd_time(args),
    "open": lambda args: cmd_open(args),
    "note": lambda args: cmd_note(args),
    "calc": lambda args: cmd_calc(args),
    "sysinfo": lambda args: cmd_sysinfo(args),
    "clean": lambda args: cmd_clean(args),
    "battery": lambda args: cmd_battery(args),
    "network": lambda args: cmd_network(args),
    "convert": lambda args: cmd_convert(args),
    "random": lambda args: cmd_random(args),
    "remind": lambda args: cmd_remind(args),
    # Aliases
    "calc history": lambda args: cmd_calc_history(args),
    "clear": lambda args: cmd_clear(),
    "cls": lambda args: cmd_clear(), 
    "fun": lambda args: cmd_fun(args),
    "fun joke": lambda args: cmd_fun(["joke"]),
    "fun quote": lambda args: cmd_fun(["quote"]),
}

# --- PARSING ---
def parse_command(line: str):
    # Handle multi-word commands (like "calc history", "fun quote")
    
    # Try two-word commands first
    parts = shlex.split(line, posix=False)
    if len(parts) >= 2:
        cmd_two_word = parts[0].lower() + " " + parts[1].lower()
        if cmd_two_word in COMMAND_MAP:
            return cmd_two_word, parts[2:]
            
    # Fall back to single-word commands
    if not parts:
        return None, []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args

# --- MAIN LOOP ---

def display_banner():
    """Displays an ASCII banner for the bot."""
    # A simple, modern ASCII Art Banner (Using Rich for color)
    banner = [
        "[bold cyan]  _____   _    ____   ___   _  __ [/bold cyan]",
        "[bold cyan] |  __ \\ | |  / __ \\ / _ \\ | |/ / [/bold cyan]",
        "[bold cyan] | |  | || | | |  | | | | || ' /  [/bold cyan]",
        "[bold cyan] | |  | || | | |  | | | | ||  <   [/bold cyan]",
        "[bold cyan] | |__| || | | |__| | |_| || . \\  [/bold cyan]",
        "[bold cyan] |_____/ |_|  \\____/ \\___/ |_|\\_\\ [/bold cyan]",
        "[bold yellow] Local Assistant Bot - v2.0 - Built for Khalil [/bold yellow]"
    ]
    rprint(Panel("\n".join(banner), border_style="bold green"))
    rprint("[bold white]Ready. Type [yellow]'help'[/yellow] for commands or [yellow]'exit'[/yellow] to quit.[/bold white]")


def main():
    display_banner()
    while True:
        try:
            line = console.input("[bold magenta]>> [/bold magenta]").strip()
        except (EOFError, KeyboardInterrupt):
            rprint("\n[bold red]Exiting. Goodbye![/bold red]")
            break
        
        if not line:
            continue
        
        cmd, args = parse_command(line)
        
        if cmd in ("exit", "quit"):
            rprint("[bold red]Goodbye![/bold red]")
            break
        
        handler = COMMAND_MAP.get(cmd)
        
        if handler:
            # Command handlers print directly to console (return None or empty string)
            handler(args)
        else:
            console.print(f"[bold red]❌ Unknown command: '{line}'. Type 'help' to see available commands.[/bold red]")

if __name__ == "__main__":
    main()
