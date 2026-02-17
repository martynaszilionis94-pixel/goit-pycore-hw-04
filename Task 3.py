import sys
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)


def print_directory_tree(directory: str) -> None:
    root = Path(directory)

    if not root.exists():
        print("Error: path does not exist.")
        return

    if not root.is_dir():
        print("Error: path is not a directory.")
        return

    def walk(current: Path, prefix: str = "") -> None:
        items = sorted(current.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))

        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            branch = "└── " if is_last else "├── "
            next_prefix = prefix + ("    " if is_last else "│   ")

            if item.is_dir():
                print(f"{prefix}{branch}{Fore.CYAN}{item.name}{Style.RESET_ALL}")
                walk(item, next_prefix)
            else:
                print(f"{prefix}{branch}{Fore.GREEN}{item.name}{Style.RESET_ALL}")

    print(f"{Fore.CYAN}{root.name}{Style.RESET_ALL}")
    walk(root)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task3.py <directory_path>")
    else:
        print_directory_tree(sys.argv[1])

