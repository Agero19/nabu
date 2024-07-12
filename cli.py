import os
import re
from argparse import ArgumentParser, Namespace
from typing import List
from colorama import Fore, Style, init

def parse_arguments() -> Namespace:
    parser = ArgumentParser(description='Simple text pattern matching', epilog='help text', usage='script "regex" <path/to/the/file>')
    parser.add_argument("pattern", help='pattern to search')
    parser.add_argument("files", nargs='*', help='positional argument, path to the file/s')
    parser.add_argument('-c', '--count', action='store_true', help='count matched lines')
    parser.add_argument('-i', '--ignore', action='store_true', help='case insensitive search')
    parser.add_argument('-v', '--invert', action='store_true', help='exclude matched lines, search invertion')
    return parser.parse_args()

def match_file(pattern: str, files: str, counter=False, caseIgnore=False, invert=False) -> None:
    if caseIgnore:
        regex = re.compile(pattern, re.IGNORECASE)
    else:
        regex = re.compile(pattern)
    
    total_count: int = 0 

    def match_line(line):
        return bool(regex.search(line)) != invert
    
    for file in files:
        filename = os.path.basename(file)

        with open(file, 'r') as f:
            local_count: int = 0
            for idx, line in enumerate(f):
                if match_line(line):
                    local_count += 1
                    # Replace matched patterns with colored versions
                    colored_line = regex.sub(f"{Fore.MAGENTA}{Style.BRIGHT}\\g<0>{Style.RESET_ALL}", line)
                    # Colorize the filename and line count
                    print(f"{Fore.GREEN}{filename}{Style.RESET_ALL} {Fore.CYAN}{idx}{Style.RESET_ALL}: {colored_line}", end='')
                    total_count += 1
            if counter:
                print(f"{Fore.GREEN}{filename}{Style.RESET_ALL}: {Fore.MAGENTA}{local_count}{Style.RESET_ALL} matched lines in the file")
    if total_count == 0: 
        print(f"{Fore.RED}pattern don't match in {[os.path.basename(file) for file in files]}{Style.RESET_ALL}")
    elif counter:
        print(f"Total number of matching patterns is {Fore.MAGENTA}{total_count}{Style.RESET_ALL}")

def main():
    init(autoreset=True)  # Initialize colorama
    args = parse_arguments()
    if args:
        match_file(pattern=args.pattern,
                     files=args.files, 
                     counter=args.count, 
                     caseIgnore=args.ignore, 
                     invert=args.invert)
    else: 
        print("No arguments provided")

if __name__ == '__main__':
    main()
