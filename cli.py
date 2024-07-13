import os
from pathlib import Path
import re
from argparse import ArgumentParser, Namespace
from typing import List
from colorama import Fore, Style, init

def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        description='Simple text pattern matching',
        epilog='help text', 
        usage='script "regex" <path/to/the/file>'
    )
    parser.add_argument("pattern", help='pattern to search')
    parser.add_argument("files", nargs='*', help='positional argument, path to the file/s')
    parser.add_argument('-c', '--count', action='store_true', help='count matched lines')
    parser.add_argument('-i', '--ignore', action='store_true', help='case insensitive search')
    parser.add_argument('-v', '--invert', action='store_true', help='exclude matched lines, search invertion')
    parser.add_argument('-r', '--recursive', action='store_true', help='recursive search over directories')

    return parser.parse_args()

def compile_pattern(pattern: str, case_ignore: bool) -> re.Pattern:
    """Compile regex pattern depending on case insensitivity flag"""
    if case_ignore:
        return re.compile(pattern, re.IGNORECASE)
    return re.compile(pattern)

def process_line(line: str, pattern: re.Pattern, invert: bool) -> bool:
    """Check if line matches the pattern , considering inversion"""
    return bool(pattern.search(line)) != invert

def colorise_line(line: str, pattern: re.Pattern) -> str:
    """Replace matched patterns in the given line with colorized formats"""
    return pattern.sub(f"{Fore.MAGENTA}{Style.BRIGHT}\\g<0>{Style.RESET_ALL}", line)

def match_file(pattern: str, files: List[str], count: bool = False, case_ignore: bool = False, invert: bool = False) -> None:
    regex = compile_pattern(pattern, case_ignore)
    total_count: int = 0

    for file_path in files:
        try:
            file = Path(file_path)
            filename = file.name
            local_count: int = 0

            with open(file, 'r') as f:
                for idx, line in enumerate(f):
                    if process_line(line, regex, invert):
                        local_count += 1
                        colored_line = colorise_line(line, regex)
                        print(f"{Fore.GREEN}{filename}{Style.RESET_ALL} {Fore.CYAN}{idx}{Style.RESET_ALL}: {colored_line}", end='')
                        total_count += 1

                if count:
                    print(f"{Fore.GREEN}{filename}{Style.RESET_ALL}: {Fore.MAGENTA}{local_count}{Style.RESET_ALL} matched lines in the file")

        except FileNotFoundError:
            print(print(f"{Fore.RED}File not found: {file_path}{Style.RESET_ALL}"))
        except Exception as e:
            print(f"{Fore.RED}Error reading file {file_path}: {e}{Style.RESET_ALL}")

    if total_count == 0:
        print(f"{Fore.RED}Pattern doesn't match in {[Path(file).name for file in files]}{Style.RESET_ALL}")
    elif count:
        print(f"Total number of matching patterns is {Fore.MAGENTA}{total_count}{Style.RESET_ALL}")

def main():
    init(autoreset=True)  # Initialize colorama
    args = parse_arguments()
    if args:
        match_file(
            pattern=args.pattern,
            files=args.files, 
            count=args.count, 
            case_ignore=args.ignore, 
            invert=args.invert
        )

if __name__ == '__main__':
    main()
