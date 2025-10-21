import shlex
from commands import (
    cmd_help, cmd_time, cmd_open, cmd_note, cmd_calc, cmd_sysinfo, cmd_clear
)

COMMAND_MAP = {
    "help": lambda args: cmd_help(),
    "time": lambda args: cmd_time(args),
    "open": lambda args: cmd_open(args),
    "note": lambda args: cmd_note(args),
    "calc": lambda args: cmd_calc(args),
    "sysinfo": lambda args: cmd_sysinfo(args),
    "clear": lambda args: cmd_clear(),
}

def parse_command(line: str):
    parts = shlex.split(line, posix=False)
    if not parts:
        return None, []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args

def main():
    print("Local Assistant Bot — ready. Type 'help' for commands.")
    while True:
        try:
            line = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not line:
            continue
        cmd, args = parse_command(line)
        if cmd in ("exit", "quit"):
            print("Goodbye.")
            break
        handler = COMMAND_MAP.get(cmd)
        if handler:
            output = handler(args)
            if output:
                print(output)
        else:
            print("Unknown command. Type 'help' to see available commands.")

if __name__ == "__main__":
    main()
