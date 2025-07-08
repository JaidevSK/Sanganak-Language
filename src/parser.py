from src.astDefiner import *
from src.lexer import *

class Parser:
    def __init__(self, tokens, args=[]):
        # We first initialize the parser with the list of tokens, the current index and an empty stack
        self.tokens = tokens
        self.i = 0
        self.stack = []
        self.args = args

    def parse(self):
        # This function is used to parse the tokens
        try:
            while self.i < len(self.tokens): # We iterate over the tokens
                # print("Hello")
                token = self.tokens[self.i] # We get the current token
                # print(token)
                # print(self.stack)
                if isinstance(token, StringToken): # If the token is a StringToken
                    self.stack.append(token.v) # We append the value of the token to the stack
                elif isinstance(token, NumberToken): # If the token is a NumberToken
                    self.stack.append(int(token.v)) # We append the value of the token to the stack
                elif isinstance(token, NegNumberToken): # If the token is a NegNumberToken
                    self.stack.append(-int(token.v)) # We append the value of the token to the stack
                elif isinstance(token, DecimalNumberToken): # If the token is a DecimalNumberToken
                    self.stack.append(float(token.v)) # We append the value of the token to the stack
                elif isinstance(token, NegDecimalNumberToken):  # If the token is a NegDecimalNumberToken
                    self.stack.append(-float(token.v)) # We append the value of the token to the stack
                elif isinstance(token, BoolToken): # If the token is a NumberToken
                    if token.v == "true":
                        self.stack.append(True)
                    else:
                        self.stack.append(False)
                    # self.stack.append(int(token.v)) # We append the value of the token to the stack
                elif isinstance(token, SymbolToken): # If the token is a DecimalNumberToken
                    self.stack.append(token) # We append the value of the token to the stack

                elif isinstance(token, WordToken): # If the token is a WordToken
                    if token.v == '[':
                        # print("In a list")
                        openingctr = 1
                        tokens_list = []
                        self.i += 1
                        while self.i<len(self.tokens):
                            if self.tokens[self.i] == WordToken("]"):
                                openingctr-=1
                            elif self.tokens[self.i] == WordToken("["):
                                openingctr+=1
                            if openingctr == 0:
                                # print(tokens_list)
                                p = Parser(tokens_list)
                                p.parse()
                                stk = p.stack
                                # print(stk)
                                self.stack.append(stk)
                                break
                            else:
                                tokens_list.append(self.tokens[self.i])
                                self.i+=1
                            
                    elif token.v == '+': # If the token is a plus sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int or type(num1) == float, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == int or type(num2) == float, "INVALID OPERAND TYPE"
                        self.stack.append(num1 + num2) # We append the sum of the two elements to the stack
                    elif token.v == '-': # If the token is a minus sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int or type(num1) == float, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == int or type(num2) == float, "INVALID OPERAND TYPE"
                        self.stack.append(num2 - num1) # We append the difference of the two elements to the stack
                    elif token.v == '*': # If the token is a multiplication sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int or type(num1) == float, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == int or type(num2) == float, "INVALID OPERAND TYPE"
                        self.stack.append(num1 * num2) # We append the product of the two elements to the stack
                    elif token.v == '/': # If the token is a division sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int or type(num1) == float, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == int or type(num2) == float, "INVALID OPERAND TYPE"
                        assert num1 != 0, "DIV BY ZERO" # We check if the divisor is not zero
                        self.stack.append(num2 / num1) # We append the division of the two elements to the stack
                    elif token.v == '^': # If the token is a power sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int or type(num1) == float, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == int or type(num2) == float, "INVALID OPERAND TYPE"
                        assert not(num1 <= 0 and num2 == 0), "DIV BY ZERO" # We check if the base is positive
                        self.stack.append(num2 ** num1) # We append the power of the two elements to the stack
                    elif token.v == 'get': # If the token is a get sign
                        inp_val = input() # We take the input from the user
                        if inp_val == "true":
                            self.stack.append(True)
                        elif inp_val == "false":
                            self.stack.append(False)
                        elif inp_val[0]!='"': # If the input is not a string
                            if inp_val[0] == "-": # If the input is a negative number
                                inp_val_wo_neg = inp_val[1:] # We remove the negative sign
                                if inp_val_wo_neg.isdigit(): # If the input is a digit
                                    self.stack.append(int(inp_val)) # We append the input to the stack
                                elif inp_val_wo_neg.replace('.', '', 1).isdigit(): # If the input is a decimal number
                                    self.stack.append(float(inp_val)) # We append the input to the stack
                                else: # If the input is not a number
                                    raise Exception(f"Input of Invalid type: {inp_val}") # We raise an exception
                            elif inp_val.isdigit(): # If the input is a digit
                                self.stack.append(int(inp_val)) # We append the input to the stack
                            elif inp_val.replace('.', '', 1).isdigit(): # If the input is a decimal number
                                self.stack.append(float(inp_val)) # We append the input to the stack
                            else: # If the input is not a number
                                raise Exception(f"Input of Invalid type: {inp_val}") # We raise an exception
                        else: # If the input is a string
                            if inp_val[-1] == '"': # If the input is a string
                                for i in range(1, len(inp_val)-1): # We iterate over the input
                                    if inp_val[i] == '"' and inp_val[i-1] != '\\': # If the input is a string and not an escape character, that is a discontinuity
                                        raise Exception(f"Invalid string: {inp_val}") # We raise an exception
                                self.stack.append(inp_val[1:-1]) # We append the input to the stack
                            else:
                                raise Exception(f"Invalid string: {inp_val}") # We raise an exception
                    elif token.v == 'put': # If the token is a put word
                        assert len(self.stack) > 0, "EMPTY STACK" # We check if the stack is not empty
                        # if type(self.stack[-1]) == str: # If the last element of the stack is a string
                        #     print('"', end='') # We print the " string
                        #     to_print = self.stack[-1] # We get the last element of the stack
                        #     if '\\n' in to_print: # If the string has a newline character
                        #         to_print = to_print.replace('\\n', '\n') # We replace the newline character with a newline
                        #     if '\\t' in to_print: # If the string has a tab character
                        #         to_print = to_print.replace('\\t', '\t') # We replace the tab character with a tab
                        #     if '\\\\' in to_print: # If the string has a backslash character
                        #         to_print = to_print.replace('\\\\', '\\') # We replace the backslash character with a backslash
                        #     if '\\"' in to_print: # If the string has a double quote character
                        #         to_print = to_print.replace('\\"', '"') # We replace the double quote character with a double quote
                        #     print(to_print, end='') # We print the string
                        #     print('"') # We print the string "
                        # else: # If the last element of the stack is not a string, that is a number
                        def format_value(value): # If it is not a string, we format it
                            if isinstance(value, bool):  # Format booleans
                                return "true" if value else "false" # Format boolean values
                            elif isinstance(value, list):  # Format lists
                                formatted_list = " ".join(format_value(v) for v in value)  # Recursively format nested lists
                                return f"[ {formatted_list} ]" # Format list values
                            elif isinstance(value, str):  # Format strings
                                return '"' + value + '"' # Format string values
                            elif isinstance(value, SymbolToken):
                                return "'"+value.v
                            else:  # Format numbers or other types
                                return str(value) # Format other types
                        print(format_value(self.stack[-1])) # We print the last element of the stack
                        # print(self.stack[-1]) # We print the last element of the stack
                        self.stack.pop() # We pop the last element of the stack
                    elif token.v == 'print': # Same as put for strings, without the quotes
                        assert len(self.stack) > 0, "EMPTY STACK"
                        # assert type(self.stack[-1]) == str, "INVALID OPERAND TYPE"
                        if type(self.stack[-1]) == str: # If the last element of the stack is a string
                            to_print = self.stack[-1]
                            if '\\n' in to_print:
                                to_print = to_print.replace('\\n', '\n')
                            if '\\t' in to_print:
                                to_print = to_print.replace('\\t', '\t')
                            if '\\\\' in to_print:
                                to_print = to_print.replace('\\\\', '\\')
                            if '\\"' in to_print:
                                to_print = to_print.replace('\\"', '"')
                            print(to_print)
                            self.stack.pop()
                        else: # If the last element of the stack is not a string, that is a number
                            print(self.stack[-1])
                            self.stack.pop()
                    elif token.v == 'pop': # If the token is a pop word
                        assert len(self.stack) > 0, "EMPTY STACK" # We check if the stack is not empty
                        self.stack.pop() # We pop the last element of the stack
                    elif token.v == 'dup': # If the token is a dup word
                        assert len(self.stack) > 0, "EMPTY STACK" # We check if the stack is not empty
                        self.stack.append(self.stack[-1]) # We append the last element of the stack to the stack
                    elif token.v == 'rot': # If the token is a rot word
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop() # We pop the second last element of the stack
                        self.stack.append(num1) # We append the last element of the stack to the stack
                        self.stack.append(num2) # We append the second last element of the stack to the stack
                    elif token.v == 'concat': # If the token is a concat word
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        assert type(self.stack[-1]) == str, "INVALID OPERAND TYPE" # We check if the last element of the stack is a string
                        assert type(self.stack[-2]) == str, "INVALID OPERAND TYPE" # We check if the second last element of the stack is a string
                        stri1 = self.stack.pop() # We pop the last element of the stack
                        stri2 = self.stack.pop() # We pop the second last element of the stack
                        self.stack.append(stri2 + stri1) # We append the concatenation of the two strings to the stack
                        # not, and, or, xor.
                    elif token.v == "not":
                        assert len(self.stack) > 0, "EMPTY STACK" # We check if the stack has more than one element
                        assert type(self.stack[-1]) == bool, "INVALID OPERAND TYPE" # We check if the last element of the stack is a string
                        b1 = self.stack.pop()
                        self.stack.append(not b1)
                    elif token.v == "or":
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        assert type(self.stack[-1]) == bool, "INVALID OPERAND TYPE" # We check if the last element of the stack is a string
                        assert type(self.stack[-2]) == bool, "INVALID OPERAND TYPE" # We check if the last element of the stack is a string
                        b1 = self.stack.pop()
                        b2 = self.stack.pop()
                        self.stack.append(b1 or b2)
                    elif token.v == "and":
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        assert type(self.stack[-1]) == bool, "INVALID OPERAND TYPE" # We check if the last element of the stack is a string
                        assert type(self.stack[-2]) == bool, "INVALID OPERAND TYPE" # We check if the last element of the stack is a string
                        b1 = self.stack.pop()
                        b2 = self.stack.pop()
                        self.stack.append(b1 and b2)
                    elif token.v == "xor":
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        assert type(self.stack[-1]) == bool, "INVALID OPERAND TYPE" # We check if the last element of the stack is a string
                        assert type(self.stack[-2]) == bool, "INVALID OPERAND TYPE" # We check if the last element of the stack is a string
                        b1 = self.stack.pop()
                        b2 = self.stack.pop()
                        self.stack.append(b1 ^ b2)
                    elif token.v == '=': # If the token is a multiplication sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int or type(num1) == float, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == int or type(num2) == float, "INVALID OPERAND TYPE"
                        self.stack.append(num1 == num2) # We append the product of the two elements to the stack
                    elif token.v == '<': # If the token is a multiplication sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int or type(num1) == float, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == int or type(num2) == float, "INVALID OPERAND TYPE"
                        self.stack.append(num1 > num2) # We append the product of the two elements to the stack
                    elif token.v == '>': # If the token is a multiplication sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int or type(num1) == float, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == int or type(num2) == float, "INVALID OPERAND TYPE"
                        self.stack.append(num1 < num2) # We append the product of the two elements to the stack
                    elif token.v == '>=': # If the token is a multiplication sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int or type(num1) == float, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == int or type(num2) == float, "INVALID OPERAND TYPE"
                        self.stack.append(num1 <= num2) # We append the product of the two elements to the stack
                    elif token.v == '<=': # If the token is a multiplication sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int or type(num1) == float, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == int or type(num2) == float, "INVALID OPERAND TYPE"
                        self.stack.append(num1 >= num2) # We append the product of the two elements to the stack
                    elif token.v == '!=': # If the token is a multiplication sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int or type(num1) == float, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == int or type(num2) == float, "INVALID OPERAND TYPE"
                        self.stack.append(num1 != num2) # We append the product of the two elements to the stack

                    elif token.v == 'nth': # If the token is a multiplication sign
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == int, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        assert type(num2) == list, "INVALID OPERAND TYPE"
                        self.stack.append(num2[num1]) # We append the product of the two elements to the stack
                    elif token.v == "argv":
                        print(self.stack)
                        self.stack.append(self.args)
                        print(self.stack)
                    elif token.v == 'spread': # If the token is a multiplication sign
                        assert len(self.stack) > 0, "EMPTY STACK" # We check if the stack has more than one element
                        num1 = self.stack.pop() # We pop the last element of the stack
                        assert type(num1) == list, "INVALID OPERAND TYPE" # We check if the type of the element is int or float
                        for elt in num1:
                            self.stack.append(elt) # We append the product of the two elements to the stack\
                    # b=, b!= for comparing Booleans.
                    elif token.v == 'b=': # For comparing Booleans, we use b= and b!=
                        assert len(self.stack) > 1, "EMPTY STACK"
                        num1 = self.stack.pop() # We pop the last element of the stack
                        num2 = self.stack.pop()
                        assert type(num1) == bool, "INVALID OPERAND TYPE"
                        assert type(num2) == bool, "INVALID OPERAND TYPE"
                        self.stack.append(num1 == num2)
                    elif token.v == 'b!=': # For comparing Booleans, we use b= and b!=
                        assert len(self.stack) > 1, "EMPTY STACK"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert type(num1) == bool, "INVALID OPERAND TYPE"
                        assert type(num2) == bool, "INVALID OPERAND TYPE"
                        self.stack.append(num1 != num2)

                    # Add s= and s!= for string comparison. lex<, lex>, lex<=, and lex>= for lexicographic string comparison.
                    elif token.v == 's=': # For comparing strings, we use s= and s!=
                        assert len(self.stack) > 1, "EMPTY STACK"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert type(num1) == str, "INVALID OPERAND TYPE"
                        assert type(num2) == str, "INVALID OPERAND TYPE"
                        self.stack.append(num1 == num2)
                    elif token.v == 's!=': # For comparing strings, we use s= and s!=
                        assert len(self.stack) > 1, "EMPTY STACK"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert type(num1) == str, "INVALID OPERAND TYPE"
                        assert type(num2) == str, "INVALID OPERAND TYPE"
                        self.stack.append(num1 != num2)
                    elif token.v == 'lex>': # For comparing strings, we use lex<, lex>, lex<=, and lex>=
                        assert len(self.stack) > 1, "EMPTY STACK"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert type(num1) == str, "INVALID OPERAND TYPE"
                        assert type(num2) == str, "INVALID OPERAND TYPE"
                        self.stack.append(num1 < num2)
                    elif token.v == 'lex<': # For comparing strings, we use lex<, lex>, lex<=, and lex>=
                        assert len(self.stack) > 1, "EMPTY STACK"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert type(num1) == str, "INVALID OPERAND TYPE"
                        assert type(num2) == str, "INVALID OPERAND TYPE"
                        self.stack.append(num1 > num2)
                    elif token.v == 'lex>=': # For comparing strings, we use lex<, lex>, lex<=, and lex>=
                        assert len(self.stack) > 1, "EMPTY STACK"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert type(num1) == str, "INVALID OPERAND TYPE"
                        assert type(num2) == str, "INVALID OPERAND TYPE"
                        self.stack.append(num1 <= num2)
                    elif token.v == 'lex<=': # For comparing strings, we use lex<, lex>, lex<=, and lex>=
                        assert len(self.stack) > 1, "EMPTY STACK"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert type(num1) == str, "INVALID OPERAND TYPE"
                        assert type(num2) == str, "INVALID OPERAND TYPE"
                        self.stack.append(num1 >= num2)
                    # Some list manipulation
                        # len
                        # [ x1 xn ] S to n S
                        # listn
                        # n xn x1 S to [ x1 xn ] S.
                        # list
                        # Turns all values in stack into a list.
                    elif token.v == 'len': # If the token is a len word
                        assert len(self.stack) > 0, "EMPTY STACK" # We check if the stack is not empty
                        num1 = self.stack.pop() # We pop the last element of the stack
                        assert type(num1) == list, "INVALID OPERAND TYPE" # We check if the last element of the stack is a list
                        self.stack.append(len(num1)) # We append the length of the list to the stack
                    elif token.v == 'list': # If the token is a list word
                        # dummy = []
                        # while len(self.stack) > 0:
                        #     dummy.append(self.stack.pop())
                        # while len(dummy) > 0:
                        #     self.stack.append([dummy.pop()])
                        self.stack = list([self.stack]) # We append the list of the stack to the stack

                    elif token.v == 'listn': # If the token is a listn word
                        assert len(self.stack) > 0, "EMPTY STACK" # We check if the stack is not empty
                        num1 = self.stack.pop() # We pop the last element of the stack
                        assert type(num1) == int, "INVALID OPERAND TYPE" # We check if the last element of the stack is an int
                        dummy = [] # We create a dummy list
                        for i in range(num1): # We iterate over the range of the number
                            dummy.append(self.stack.pop()) # We pop the last element of the stack
                        dummy.reverse() # We reverse the dummy list
                        self.stack.append(dummy) # We append the dummy list to the stack


                    elif token.v == '{':  # Start of a stored procedure
                        opening_ctr = 1 # Counter for the opening braces
                        tokens_list = [] # List to store the tokens of the procedure
                        self.i += 1 # Increment the index to skip the opening brace
                        while self.i < len(self.tokens): # While we are not at the end of the tokens
                            if self.tokens[self.i] == WordToken("}"): # If we find a closing brace
                                opening_ctr -= 1 # Decrement the counter
                            elif self.tokens[self.i] == WordToken("{"): # If we find an opening brace
                                opening_ctr += 1 # Increment the counter
                            if opening_ctr == 0: # If the counter is zero, we have found the matching closing brace
                                self.stack.append(tokens_list)  # Push the stored procedure as a list of tokens
                                break # Break the loop
                            else: # If we are not at the end of the procedure
                                tokens_list.append(self.tokens[self.i]) # Append the token to the list
                                self.i += 1 # Increment the index to the next token

                    elif token.v == 'run':  # Execute the stored procedure on top of the stack
                        assert len(self.stack) > 0, "EMPTY STACK" # We check if the stack is not empty
                        procedure = self.stack.pop() # We pop the last element of the stack
                        assert type(procedure) == list, "INVALID OPERAND TYPE" # We check if the last element of the stack is a list
                        p = Parser(procedure) # We create a new parser for the procedure
                        p.parse() # We parse the procedure
                        self.stack.extend(p.stack)  # Merge the resulting stack back

                    elif token.v == 'if':  # Conditional execution
                        assert len(self.stack) > 2, "EMPTY STACK" # We check if the stack has more than two elements
                        else_proc = self.stack.pop() # We pop the last element of the stack
                        then_proc = self.stack.pop() # We pop the second last element of the stack
                        condition = self.stack.pop() # We pop the third last element of the stack
                        # print(else_proc, then_proc, condition)
                        assert type(condition) == bool, "INVALID OPERAND TYPE" # We check if the last element of the stack is a boolean
                        assert type(then_proc) == list and type(else_proc) == list, "INVALID OPERAND TYPE" # We check if the last element of the stack is a list
                        if condition: # If the condition is true
                            # print("SELECTED", then_proc)
                            p = Parser(then_proc) # We create a new parser for the then procedure
                        else: # If the condition is false
                            # print("SELECTED", else_proc)
                            p = Parser(else_proc) # We create a new parser for the else procedure

                        p.functions = self.functions  # Inherit function definitions
                        p.variables = self.variables  # Inherit variable definitions
                        p.stack = self.stack  # Inherit the stack
                        p.args = self.args

                        p.parse() # We parse the procedure
                        self.stack.extend(p.stack) # We merge the resulting stack back
                        self.functions.update(p.functions)
                        self.variables.update(p.variables)

                    elif token.v == 'repeat':  # Repeat a procedure N times
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        procedure = self.stack.pop() # We pop the last element of the stack
                        n = self.stack.pop() # We pop the second last element of the stack
                        assert type(n) == int and n >= 0, "INVALID OPERAND TYPE" # We check if the last element of the stack is a positive integer
                        assert type(procedure) == list, "INVALID OPERAND TYPE" # We check if the last element of the stack is a list
                        for _ in range(n): # We repeat the procedure n times
                            p = Parser(procedure) # We create a new parser for the procedure
                            p.functions = self.functions  # Inherit function definitions
                            p.variables = self.variables  # Inherit variable definitions
                            p.stack = self.stack  # Inherit the stack

                            p.parse() # We parse the procedure
                            self.stack.extend(p.stack) # We merge the resulting stack back
                            self.functions.update(p.functions)
                            self.variables.update(p.variables)

                    elif token.v == 'while':  # While loop CHECK THIS. THIS IS WRONG
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        body_proc = self.stack.pop()  # Pop the body procedure (B) FIRST
                        condition_proc = self.stack.pop()  # Pop the condition procedure (C) SECOND
                        # print("Condition proc:", condition_proc)  # Debugging output
                        # print("Body proc:", body_proc)  # Debugging output                        
                        assert type(condition_proc) == list and type(body_proc) == list, "INVALID OPERAND TYPE" # We check if the last element of the stack is a list
                        # Condition and Body do not have the body of the stack and tokens with them
                        # We need to add them to the stack and tokens of the parser
                        stack_copy = self.stack.copy()  # Copy the current stack
                        cp = Parser(condition_proc)  # Create a new parser for the condition
                        # Extend the stack with the current stack
                        cp.stack.extend(stack_copy) # Extend the condition stack with the current stack
                        bp = Parser(body_proc)  # Create a new parser for the body
                        # Extend the stack with the current stack
                        bp.stack.extend(stack_copy) # Extend the body stack with the current stack
                        # print("Condition stack:", cp.stack)  # Debugging output
                        # print("Body stack:", bp.stack)  # Debugging output
                        while True:
                            # Parse the condition
                            cp = Parser(condition_proc)  # Create a new parser for the condition
                            cp.stack.extend(self.stack)  # Extend the condition stack with the current stack
                            cp.parse()  # Parse the condition
                            # Extend the condition stack with the current stack
                            # print("Condition stack after parsing:", cp.stack)  # Debugging output
                            # Check the condition
                            condition = cp.stack.pop()
                            # print("Condition:", condition)  # Debugging output
                            # print(type(condition))  # Debugging output
                            assert type(condition) == bool, "INVALID OPERAND TYPE"
                            if not condition:  # If the condition is false, break the loop
                                break
                            # Parse the body
                            # print("Body Proc:", body_proc)  # Debugging output
                            bp = Parser(body_proc)
                            bp.stack.extend(self.stack)
                            # print("Body stack before parsing:", bp.stack)  # Debugging output
                            bp.parse()
                            # print("Body stack after parsing:", bp.stack)  # Debugging output
                            cp.stack = bp.stack.copy()  # Copy the body stack to the condition stack
                            # Reset the body stack for the next iteration
                            # print("Conditional stack after copying:", cp.stack)  # Debugging output
                            self.stack = cp.stack.copy()  # Copy the condition stack to the main stack
                            # print("Main stack after copying:", self.stack)  # Debugging output
                            # print(condition_proc)
                    elif token.v == 'inc':  # Increment the top value of the stack
                        assert len(self.stack) > 0, "EMPTY STACK"
                        num = self.stack.pop()
                        assert type(num) == int, "INVALID OPERAND TYPE"
                        self.stack.append(num + 1)
                    elif token.v == 'dec':  # Decrement the top value of the stack
                        assert len(self.stack) > 0, "EMPTY STACK"
                        num = self.stack.pop()
                        assert type(num) == int, "INVALID OPERAND TYPE"
                        self.stack.append(num - 1)

                    # Quiz 3
                    elif token.v == 'is-number?':  # Check if the top value is a number
                        assert len(self.stack) > 0, "EMPTY STACK"
                        num = self.stack.pop()
                        self.stack.append(isinstance(num, (int, float)))
                    elif token.v == 'is-list?': # Check if the top of the stack is a list
                        assert len(self.stack) > 0, "EMPTY STACK"
                        num = self.stack.pop()
                        self.stack.append(isinstance(num, list))
                    elif token.v == 'is-string?':  # Check if the top value is a string
                        assert len(self.stack) > 0, "EMPTY STACK"
                        num = self.stack.pop()
                        self.stack.append(isinstance(num, str))
                    elif token.v == 'is-bool?':  # Check if the top value is a string
                        assert len(self.stack) > 0, "EMPTY STACK"
                        num = self.stack.pop()
                        self.stack.append(isinstance(num, bool))

                    elif token.v == 'forever':  # While loop CHECK THIS. THIS IS WRONG
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        body_proc = self.stack.pop()  # Pop the body procedure (B) FIRST
                        # print("Condition proc:", condition_proc)  # Debugging output
                        # print("Body proc:", body_proc)  # Debugging output                        
                        assert type(body_proc) == list, "INVALID OPERAND TYPE" # We check if the last element of the stack is a list
                        # Condition and Body do not have the body of the stack and tokens with them
                        # We need to add them to the stack and tokens of the parser
                        stack_copy = self.stack.copy()  # Copy the current stack
                        bp = Parser(body_proc)  # Create a new parser for the body
                        # Extend the stack with the current stack
                        bp.stack.extend(stack_copy) # Extend the body stack with the current stack
                        # print("Condition stack:", cp.stack)  # Debugging output
                        # print("Body stack:", bp.stack)  # Debugging output
                        while True:
                            # Parse the condition
                            # Extend the condition stack with the current stack
                            # print("Condition stack after parsing:", cp.stack)  # Debugging output
                            # Check the condition
                            condition = True
                            # print("Condition:", condition)  # Debugging output
                            # print(type(condition))  # Debugging output
                            assert type(condition) == bool, "INVALID OPERAND TYPE"
                            if not condition:  # If the condition is false, break the loop
                                break
                            # Parse the body
                            # print("Body Proc:", body_proc)  # Debugging output
                            bp = Parser(body_proc)
                            bp.stack.extend(self.stack)
                            # print("Body stack before parsing:", bp.stack)  # Debugging output
                            bp.parse()
                            # print("Body stack after parsing:", bp.stack)  # Debugging output
                            cp_stack = bp.stack.copy()  # Copy the body stack to the condition stack
                            # # Reset the body stack for the next iteration
                            # # print("Conditional stack after copying:", cp.stack)  # Debugging output
                            self.stack = cp_stack.copy()  # Copy the condition stack to the main stack
                            # print("Main stack after copying:", self.stack)  # Debugging output
                            # print(condition_proc)


                    elif token.v == 'foreach':  # While loop CHECK THIS. THIS IS WRONG
                        assert len(self.stack) > 1, "EMPTY STACK" # We check if the stack has more than one element
                        list_on = self.stack.pop()  # Pop the body procedure (B) FIRST
                        body_on = self.stack.pop()  # Pop the condition procedure (C) SECOND
                        # print("Condition proc:", condition_proc)  # Debugging output
                        # print("Body proc:", body_proc)  # Debugging output                        
                        assert type(body_on) == list and type(list_on) == list, "INVALID OPERAND TYPE" # We check if the last element of the stack is a list
                        for i in list_on:
                            bp = Parser(body_on)
                            bp.stack.append(i)
                            bp.parse()

                    elif token.v == 'is-symbol?':  # Check if the top value is a symbol
                        assert len(self.stack) > 0, "EMPTY STACK"
                        num1 = self.stack.pop()
                        self.stack.append(isinstance(num1, SymbolToken))

                    elif token.v == 'sym=':
                        assert len(self.stack) > 1, "EMPTY STACK"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, SymbolToken), "INVALID OPERAND TYPE"
                        assert isinstance(num2, SymbolToken), "INVALID OPERAND TYPE"
                        self.stack.append(num1 == num2)
                    elif token.v == 'def':  # Define a function
                        assert len(self.stack) > 1, "EMPTY STACK"
                        symbol = self.stack.pop()
                        procedure = self.stack.pop()
                        assert isinstance(symbol, SymbolToken), "INVALID OPERAND TYPE: Symbol expected"
                        assert isinstance(procedure, list), "INVALID OPERAND TYPE: Procedure expected"
                        if not symbol.v:
                            raise Exception("Empty symbols are not allowed")
                        # Store the function definition in the global dictionary
                        self.functions[symbol.v] = procedure
                    else:
                        # print(self.variables)
                        # print(self.functions)
                        # Check if the token is a defined function
                        if token.v in self.functions:
                            # print(token.v)
                            procedure = self.functions[token.v]
                            # print(procedure)
                            p = Parser(procedure, self.args)
                            p.functions = self.functions  # Inherit function definitions
                            p.variables = self.variables  # Inherit variable definitions
                            p.stack = self.stack  # Inherit the stack
                            # print(p.stack, "\n\n", p.functions, "\n\n", p.variables)
                            p.parse()
                            self.stack = p.stack  # Update the stack
                        elif token.v in self.variables:
                            # If the token is a defined variable, push its value onto the stack
                            self.stack.append(self.variables[token.v])
                        else:
                            raise Exception(f"Unknown token or function: {token.v}")
                self.i += 1
        except Exception as e:
            print(e)

    # Initialize a dictionary to store function definitions
    functions = {}
    # Initialize a dictionary to store global variables
    variables = {}