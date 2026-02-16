"""
Тема 6. Домашня робота (goit-pycore-hw-04)
Завдання 1-4 в одному файлі.

Як використовувати:
1) Імпортувати функції (task 1-2) у свої тести/скрипти:
   from main import total_salary, get_cats_info

2) Завдання 3 (візуалізація директорії):
   python main.py tree /absolute/path/to/dir

3) Завдання 4 (бот):
   python main.py bot
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ---------- Task 1 ----------


def total_salary(path: str) -> Tuple[int, float]:
    """
    Reads salary file where each line is: "Full Name,Salary"
    Returns: (total_salary, average_salary)
    Handles missing file and bad data.
    """
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) != 2:
                    # bad format line
                    continue

                name, salary_str = parts[0].strip(), parts[1].strip()
                if not name:
                    continue

                try:
                    salary = int(salary_str)
                except ValueError:
                    continue

                total += salary
                count += 1

    except FileNotFoundError:
        # file not found
        return 0, 0.0
    except OSError:
        # other file read errors
        return 0, 0.0

    average = (total / count) if count else 0.0
    return total, average


# ---------- Task 2 ----------


def get_cats_info(path: str) -> List[Dict[str, str]]:
    """
    Reads cats file where each line is: "id,name,age"
    Returns list of dicts: {"id": "...", "name": "...", "age": "..."}
    Handles missing file and bad data.
    """
    cats: List[Dict[str, str]] = []

    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) != 3:
                    continue

                cat_id, name, age = (p.strip() for p in parts)
                if not cat_id or not name or not age:
                    continue

                cats.append({"id": cat_id, "name": name, "age": age})

    except FileNotFoundError:
        return []
    except OSError:
        return []

    return cats


# ---------- Task 3 ----------

def _safe_init_colorama():
    """
    Initializes colorama if available; if not installed, works without colors.
    """
    try:
        from colorama import init  # type: ignore
        init(autoreset=True)
        return True
    except Exception:
        return False


def _colors():
    """
    Returns (DIR_COLOR, FILE_COLOR, RESET) depending on colorama availability.
    """
    try:
        from colorama import Fore, Style  # type: ignore
        return Fore.CYAN, Fore.GREEN, Style.RESET_ALL
    except Exception:
        return "", "", ""


def print_directory_tree(directory: str) -> None:
    """
    Prints a directory structure with different colors for directories and files.
    Uses pathlib. Handles path errors.
    """
    _safe_init_colorama()
    DIR_COLOR, FILE_COLOR, RESET = _colors()

    root = Path(directory)

    if not root.exists():
        print("Error: path does not exist.")
        return
    if not root.is_dir():
        print("Error: path is not a directory.")
        return

    def walk(current: Path, prefix: str = "") -> None:
        items = sorted(current.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        for idx, item in enumerate(items):
            is_last = idx == len(items) - 1
            branch = "└── " if is_last else "├── "
            next_prefix = prefix + ("    " if is_last else "│   ")

            if item.is_dir():
                print(f"{prefix}{branch}{DIR_COLOR}{item.name}{RESET}")
                walk(item, next_prefix)
            else:
                print(f"{prefix}{branch}{FILE_COLOR}{item.name}{RESET}")

    print(f"{DIR_COLOR}{root.name}{RESET}")
    walk(root)


# ---------- Task 4 (CLI bot) ----------

def parse_input(user_input: str):
    """
    Splits user input into command and args.
    Commands are case-insensitive.
    """
    user_input = user_input.strip()
    if not user_input:
        return "", []
    cmd, *args = user_input.split()
    return cmd.strip().lower(), args


def add_contact(args, contacts: Dict[str, str]) -> str:
    if len(args) != 2:
        return "Usage: add <name> <phone>"
    name, phone = args
    contacts[name] = phone
    return "Contact added."


def change_contact(args, contacts: Dict[str, str]) -> str:
    if len(args) != 2:
        return "Usage: change <name> <phone>"
    name, phone = args
    if name not in contacts:
        return "Error: contact not found."
    contacts[name] = phone
    return "Contact updated."


def show_phone(args, contacts: Dict[str, str]) -> str:
    if len(args) != 1:
        return "Usage: phone <name>"
    name = args[0]
    if name not in contacts:
        return "Error: contact not found."
    return contacts[name]


def show_all(contacts: Dict[str, str]) -> str:
    if not contacts:
        return "No contacts saved."
    lines = [f"{name}: {phone}" for name, phone in contacts.items()]
    return "\n".join(lines)


def main_bot() -> None:
    contacts: Dict[str, str] = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "":
            print("Invalid command.")
        else:
            print("Invalid command.")


# ---------- Entry point ----------

def _print_usage() -> None:
    print(
        "Usage:\n"
        "  python main.py bot\n"
        "  python main.py tree <path_to_directory>\n"
        "\n"
        "Tasks 1-2 are functions:\n"
        "  total_salary(path)\n"
        "  get_cats_info(path)\n"
    )


def main() -> None:
    if len(sys.argv) < 2:
        _print_usage()
        return

    mode = sys.argv[1].strip().lower()

    if mode == "bot":
        main_bot()
    elif mode == "tree":
        if len(sys.argv) < 3:
            print("Error: missing directory path.")
            _print_usage()
            return
        print_directory_tree(sys.argv[2])
    else:
        _print_usage()


if __name__ == "__main__":
    main()
