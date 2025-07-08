from dataclasses import dataclass
from src.astDefiner import *

# In this part, we define the tokens that will be used in the lexer
# We will lex the input string and return a list of tokens

class Token: # Token class
    pass


@dataclass
class NumberToken(Token):
    # This class is used to define the token for numbers
    v: str

@dataclass
class NegNumberToken(Token):
    # This class is used to define the token for negative numbers
    v: str

@dataclass
class DecimalNumberToken(Token):
    # This class is used to define the token for decimal numbers
    v: str

@dataclass
class NegDecimalNumberToken(Token):
    # This class is used to define the token for negative decimal numbers
    v: str

@dataclass
class StringToken(Token):
    # This class is used to define the token for strings
    v: str

@dataclass
class WordToken(Token):
    # This class is used to define the token for words
    v: str

@dataclass
class BoolToken(Token):
    # This class is used to define the token for words
    v: str

@dataclass
class SymbolToken(Token):
    # This class is used to define the token for symbols
    v: str


    


    # +, -, *, /, ^ for arithmetic.
    # get for reading a value (number or string from input) from keyboard. The read value is pushed to stack.
    # put for printing a value (followed by newline) to screen.
    # pop for removing top element from stack.
    # dup for turning stack from x S to x x S.
    # rot for turning stack from x y S to y x S.
    # concat for concatenating two strings.
    # print for printing a string to screen.

def lex(s):
    # This function is used to lex the input string and return a list of tokens
    tokens = [] # List of tokens
    i = 0 # Index of the current character
    while i < len(s): # Loop through the input string
        if s.isspace() or s[i] == '\n': # If the character is a space or a newline, skip it
            i += 1 # Increment the index
            continue # Continue to the next iteration of the loop
        elif s[i].isdigit(): # If the character is a digit
            dig = '' # Initialize an empty string
            is_decimal = False # Initialize a boolean variable to keep track of whether the number is a decimal number
            # Loop through the input string while the character is a digit or a decimal point
            while i < len(s) and s[i].isdigit() or s[i] == '.':
                if s[i] == '.' and is_decimal: # If the number is already a decimal number and we encounter another decimal point, raise an exception
                    raise Exception("अवैध दशमांश संख्या")
                elif s[i] == '.' and is_decimal == False: # If the number is not a decimal number and we encounter a decimal point, set the is_decimal variable to True
                    is_decimal = True
                dig += s[i] # Append the character to the string
                i += 1 # Increment the index
            if is_decimal: # If the number is a decimal number
                tokens.append(DecimalNumberToken(dig))
                assert i == len(s) or s[i].isspace() or s[i] == '\n', "अवैध संख्या"
            else:
                tokens.append(NumberToken(dig))
                assert i == len(s) or s[i].isspace() or s[i] == '\n', "अवैध संख्या"

        elif s[i] == '-' and i+1 < len(s) and s[i+1].isdigit(): # If the character is a negative sign and the next character is a digit
            i += 1 # Increment the index
            dig = '' # Initialize an empty string
            is_decimal = False # Initialize a boolean variable to keep track of whether the number is a decimal number
            while i < len(s) and s[i].isdigit() or s[i] == '.': # Loop through the input string while the character is a digit or a decimal point
                if s[i] == '.' and is_decimal: # If the number is already a decimal number and we encounter another decimal point, raise an exception
                    raise Exception("अवैध दशमांश संख्या")
                elif s[i] == '.' and is_decimal == False: # If the number is not a decimal number and we encounter a decimal point, set the is_decimal variable to True
                    is_decimal = True 
                dig += s[i] # Append the character to the string
                i += 1 # Increment the index
            if is_decimal: # If the number is a decimal number
                tokens.append(NegDecimalNumberToken(dig))
                assert i == len(s) or s[i].isspace() or s[i] == '\n', "अवैध संख्या"
            else:
                tokens.append(NegNumberToken(dig))
                assert i == len(s) or s[i].isspace() or s[i] == '\n', "अवैध संख्या"

        elif s[i] == '"': # If the character is a double quote
            i += 1 # Increment the index
            string = '' # Initialize an empty string
            # while i < len(s) and s[i] != '"' and s[i] != '\n': # Loop through the input string while the character is not a double quote or a newline
            while i < len(s) and s[i] != '\n': # Loop through the input string while the character is not a double quote or a newline
                if s[i] == '"' and s[i-1] != '\\': # If the character is a double quote and the previous character is not a backslash, break the loop
                    break # Break the loop
                elif s[i] == '"' and s[i-1] == '\\': # If the character is a double quote and the previous character is a backslash, append the character to the string as this is an escaped double quote
                    string += s[i]
                    i+=1
                    continue
                string += s[i] # Append the character to the string
                i += 1 # Increment the index
            if i == len(s)-1 and s[i] != '"':
                raise Exception("अवैध स्ट्रिंग")
            assert s[i] == '"', "अवैध स्ट्रिंग"
            tokens.append(StringToken(string)) # Append the token to the list of tokens
            i += 1 # Increment the index
        
        elif s[i] == "'": # If the character is a single quote
            i += 1 # Increment the index
            symbol = '' # Initialize an empty string
            while i < len(s) and not s[i].isspace(): # Loop through the input string while the character is not a space
                symbol += s[i] # Append the character to the string
                i += 1 # Increment the index
            tokens.append(SymbolToken(symbol)) # Append the token to the list of tokens
            assert i == len(s) or s[i].isspace() or s[i] == '\n', "अवैध चिन्ह"

        else: # If the character is a word
            word = '' # Initialize an empty string
            while i < len(s) and not s[i].isspace(): # Loop through the input string while the character is not a space
                word += s[i] # Append the character to the string
                i += 1 # Increment the index
            if len(word) == 0: # If the length of the string is 0, pass
                pass # Pass
            else: # If the length of the string is not 0
                if word in ["खरे", "खोटे"]:
                    tokens.append(BoolToken(word))
                else:
                    tokens.append(WordToken(word)) # Append the token to the list of tokens
            assert i == len(s) or s[i].isspace() or s[i] == '\n', "अवैध शब्द"
            i+=1 # Increment the index
    return tokens # Return the list of tokens