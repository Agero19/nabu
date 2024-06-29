def create_table(pattern: str) -> dict:
    shift_table: dict = {}
    
    for idx,letter in enumerate(pattern):
        shift_table[letter] = len(pattern) - idx - 1
        if idx == len(pattern) - 1:
            shift_table[letter] = len(pattern)
    
    shift_table['*'] = len(pattern)

    return shift_table

def match_Pattern(text: str, pattern: str, table: dict) -> bool:
    idx: int = -1
    currentTextPos: int = len(pattern) - 1
    prev_match: bool = False 

    while currentTextPos <= len(text):
        if pattern[idx] == text[currentTextPos]:
            if abs(idx) == len(pattern):
                return True
            idx -= 1
            currentTextPos -= 1
            prev_match = True
            
        elif pattern[idx] != text[currentTextPos] and prev_match:
            currentTextPos = currentTextPos - idx - 1 + len(pattern)
            idx = -1
            prev_match = False
        elif pattern[idx] != text[currentTextPos] and text[currentTextPos] in  table.keys():
            currentTextPos += table[text[currentTextPos]]
        else:
            currentTextPos += len(pattern)

    return False
            

def main() -> None:
    text: str = "himynameisodessa"

    print(text[-1])

    pattern: str = input("Enter pattern to search: ")

    table = create_table(pattern)
    print(table)

    if match_Pattern(text, pattern, table):
        print(f"{pattern} is presented in text! Woohoo!")

#

#DONE:
# Take an input 
# Create a BMT
# Start comparing from right corner of pattern to text corresmonding letter letter
# Option 1 : match , compare one to the left
# If mismatch shift right by lenght
#Option 2: direct mismatch -> shift right by value of mismatched letter or *

#TODO:
#Output text with coloured pattern


if __name__ == "__main__":
    main()
