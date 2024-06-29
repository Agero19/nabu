from collections import defaultdict
from typing import Dict

def create_table(pattern: str) -> Dict[str, int]:
    """
    Create the bad character shift table used in Boyer-Moore string search algorithm.
    
    Args:
    - pattern (str): The pattern to search for.
    
    Returns:
    - dict: A dictionary where the keys are characters and values are the shift lengths.
    """
    shift_table: Dict[str, int] = defaultdict(lambda: len(pattern))
    
    for idx, letter in enumerate(pattern[:-1]):
        shift_table[letter] = len(pattern) - idx - 1
    
    shift_table[pattern[-1]] = len(pattern)
    shift_table['*'] = len(pattern)
    
    return shift_table

def match_pattern(text: str, pattern: str, table: Dict[str, int]) -> bool:
    """
    Check if the pattern exists in the text using the Boyer-Moore algorithm.
    
    Args:
    - text (str): The text to search within.
    - pattern (str): The pattern to search for.
    - table (dict): The bad character shift table.
    
    Returns:
    - bool: True if the pattern is found in the text, False otherwise.
    """
    pattern_len, text_len = len(pattern), len(text)
    current_pos: int = pattern_len - 1
    
    while current_pos < text_len:
        idx: int = pattern_len - 1
        while idx >= 0 and pattern[idx] == text[current_pos - (pattern_len - 1 - idx)]:
            idx -= 1
        if idx < 0:
            return True
        current_pos += table.get(text[current_pos], table['*'])
    
    return False

def main() -> None:
    """
    Main function to execute the Boyer-Moore string search.
    """
    text: str = "i am a genious i ve just coded some serious stuff"
    trimmed_text: str = "".join(text.strip().lower().split(' '))
    pattern = input("Enter pattern to search: ").strip()
    
    table = create_table(pattern)
    print("Shift Table:", table)
    
    if match_pattern(trimmed_text, pattern, table):
        print(f"'{pattern}' is present in the text! Woohoo!")
    else:
        print(f"'{pattern}' is not present in the text.")

if __name__ == "__main__":
    main()
