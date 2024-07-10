import re
from argparse import ArgumentParser, Namespace
from typing import List
from colorama import Fore, Style, init

def parse_arguments() -> Namespace:
    parser = ArgumentParser(description='Simple text pattern matching', epilog='help text', usage='script "regex" <path/to/the/file>')
    parser.add_argument("pattern", help='pattern to search')
    parser.add_argument("filename", help='positional argument')
    return parser.parse_args()

def match_pattern(pattern: str, filename: str) -> None:
    regex = re.compile(pattern)
    count: int = 0 
    with open(filename, 'r') as f:
        for idx, line in enumerate(f):
            if regex.search(line):
                # Replace matched patterns with colored versions
                colored_line = regex.sub(f"{Fore.MAGENTA}{Style.BRIGHT}\\g<0>{Style.RESET_ALL}", line)
                # Colorize the filename and line count
                print(f"{Fore.GREEN}{f.name}{Style.RESET_ALL} {Fore.CYAN}{idx}{Style.RESET_ALL}: {colored_line}", end='')
                count += 1
        if count == 0: 
            print(f"{Fore.RED}pattern don't match in {f.name}{Style.RESET_ALL}")

def main():
    init(autoreset=True)  # Initialize colorama
    args = parse_arguments()
    if args:
        match_pattern(pattern=args.pattern, filename=args.filename)
    else: 
        print("No arguments provided")

if __name__ == '__main__':
    main()
