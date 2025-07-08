from src.lexer import lex
import os


# Read the text files, lex and print the tokens
def LexerTester(filename):
    try:
        with open(filename) as f:
            s = f.read()
    except Exception as e:
        print(e)

    try:
        tokens = lex(s)
        for token in tokens:
            print(token)
    except Exception as e:
        print(e)
        return
    

# Read all the files in the folder Tests
if __name__ == "__main__":
    for filename in os.listdir("NewTests/"):
        print("Running test on file: " + filename)
        LexerTester("NewTests/" + filename)
        print("\n\n")
