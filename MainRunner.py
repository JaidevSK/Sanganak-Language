from src.parser import *
from src.lexer import *
import argparse

def Runner(filename, args):
    try:
        with open(filename) as f:
            s = f.read()
    except Exception as e:
        print(e)

    try:
        tokens = lex(s)
    except Exception as e:
        print(e)
        return
    
    try:
        p = Parser(tokens, args)
        p.parse()
    except Exception as e:
        print(e)
        return
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the parser on a file')
    parser.add_argument('filename', type=str, help='The file to run the parser on')
    parser.add_argument('args', type = str, nargs='*', help='Additional arguments for the parser')
    args = parser.parse_args()
    self_args = [args.filename] + args.args
    # print(self_args)
    Runner(args.filename, self_args)


