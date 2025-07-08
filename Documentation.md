Sanganak Language Documentation
This documentation describes the Sanganak language—a stack-based programming language—and its compiler. The goal is to help new programmers quickly learn the language, understand its design principles, and master its various constructs.

Table of Contents
Introduction
Language Philosophy and Model
Lexical Structure
Syntax and Parser Overview
Built-in Operations
Arithmetic Operators
Stack Manipulation
I/O Operation
Boolean and Comparison Operators
List Manipulation
Control Flow
Function Definition and Invocation
Type Querying
Error Handling
Extending the Language
Example Programs
Conclusion


1. Introduction
Sanganak is a stack-based programming language where all operations work on a shared stack. Instead of having named variables to pass values, most operations consume the top values from the stack and push the result back.

The language is implemented by a compiler written in Python. Its core components include a lexer, a parser, and runtime support for common operations.

2. Language Philosophy and Model
Stack-Centric: All values (numbers, strings, booleans, lists, and symbols) are maintained on a stack. Operations pop arguments from the stack and push back their results.
Minimal Syntax: Commands and procedures are defined as “words” (tokens), which get interpreted based on their type.
Procedural Execution: Code blocks (stored procedures) can be defined with delimiters and executed later.
Extensibility: The language supports user-defined functions (via the def command) and variables to allow gradual program development.

3. Lexical Structure
The compiler uses a lexer that reads the source code string and produces a list of tokens. Here are the token types:

Numeric Tokens:

NumberToken: A sequence of digits (e.g. 42).
NegNumberToken: A negative integer using a - sign (e.g. -42).
DecimalNumberToken: A floating‑point number (e.g. 3.14).
NegDecimalNumberToken: A negative decimal (e.g. -3.14).
String Tokens:

StringToken: Enclosed in double quotes (e.g. "Hello World"). The lexer allows escaped quotes.
Boolean Tokens:

BoolToken: The words true or false are read as booleans.
Symbol Tokens:

SymbolToken: Defined by a preceding single quote (e.g. 'symbol).
Word Tokens:

WordToken: Represents commands, function names, or other reserved words.
The lexer also enforces spacing and newline rules. For example, after a number token, it ensures that stop conditions (whitespace or end-of-line) are present.

4. Syntax and Parser Overview
Sanganak’s parser uses a recursive approach to scan through the token list. Here’s an outline:

Initialization:
The parser is initialized with the list of tokens and an optional argument list. It maintains:

A pointer (i) into the token list.
An execution stack (stack).
Global dictionaries (functions and variables) for user-defined functions and global variables.
Token-by-Token Parsing:
The parser loops through the tokens and:

Pushes literals: Directly pushes numbers, strings, and booleans.
Processes WordTokens: Depending on the value (the “v” field), the parser performs different operations—arithmetic, I/O, control flow, list manipulation, etc.
Procedures:
Blocks of code can be delimited using [ and ] (for lists/procedures) or with { and } (for stored procedures). The enclosed tokens are parsed recursively when executed.

Operators and Functions:
If a token does not match any built-in operation, the parser checks for user-defined functions or variables. If neither is found, an error is raised.

5. Built-in Operations
Arithmetic Operators
+: Addition
Pops two numbers from the stack. Asserts that the operands are int or float and pushes the sum.

-: Subtraction
Pops two numbers, subtracting the top element from the next, and pushes the result.

*: Multiplication
Pops two numeric values, multiplies them, and pushes the product.

/: Division
Pops two values; checks for non-zero divisor before performing division.

^: Exponentiation
Pops two numbers and computes the second token raised to the power of the first (with a check to avoid undefined cases).

Stack Manipulation
pop:
Removes the top element from the stack.

dup:
Duplicates the top value of the stack (i.e. x becomes [x, x]).

rot:
Rotates the top two stack items (swaps their order).

concat:
Pops two strings, concatenates them, and pushes the result.

I/O Operation
get:
Reads input from the user. The input is interpreted as a string, number, or boolean based on its format. For instance, a value wrapped in double quotes is recognized as a string.

put:
Prints the top element of the stack. For strings, it prints the content with proper formatting (handling escape sequences). After printing, it pops the printed value.

print:
Similar to put, but without surrounding quotes if the value is a string.

Boolean and Comparison Operators
Arithmetic Comparisons:

=: Compares two numbers for equality.
!=: Checks numerical inequality.
<, >, <=, >=: Compare numeric values. (Note that some tokens like < and > may be implemented with inverted semantics on the stack.)
Boolean Logic:

not: Logical negation (pops one boolean and pushes its inverse).
and, or, xor: Logical operations that pop two booleans and push the result.
String Comparisons:

s= and s!=: Test equality or inequality of two strings.
Lexicographic Comparisons:
lex>, lex<, lex>=, lex<=: Compare strings based on lexicographic order.
Symbol Comparison:

sym=: Compares two symbols (SymbolTokens) for equality.
is-symbol?: Checks whether the top of the stack is a symbol.

List Manipulation
List Creation and Access:

list: Wraps the current stack into a list.
listn: Pops an integer (n) and then pops n elements to form a list (the list is reversed before being pushed).
spread: Pops a list and pushes each of its elements onto the stack.
nth: Pops an integer index and a list; pushes the element at that index.
len:
Pops a list and pushes its length.

Control Flow
Procedures (Code Blocks):
Procedures described within [ and ] or { and } are stored as lists of tokens. These code blocks are not executed until explicitly parsed (e.g. using run).

run:
Pops a procedure (a list of tokens) from the stack and executes it in a new parser context. The resulting stack is then merged with the current stack.

Conditional Execution (if):
Expects three items on the stack: a condition (boolean), a “then” procedure, and an “else” procedure. Depending on the condition, the corresponding procedure gets executed.

repeat:
Pops an integer n and a procedure. The procedure is executed n times.

while:
Expects two procedures—a condition procedure and a body procedure. The condition procedure is executed and must produce a boolean. While true, the body is executed repeatedly. (Note: The parser makes copies of the stack for each loop iteration.)

forever:
Pops a procedure and enters an infinite loop executing it. Use with caution!

foreach:
Pops two items: a list and a procedure. For each element in the list, the procedure is executed with that element pushed onto the stack.

Function Definition and Invocation
Defining Functions (def):
The def command is used to define a new function. It expects a SymbolToken (as the function name) and a procedure (code block as a list of tokens). The function is stored in a global dictionary.

Invocation:
When a WordToken is encountered that matches a defined function’s name, its associated procedure is executed. The current stack, functions, and variables are inherited, ensuring consistent state between calls.

Type Querying
is-number?:
Checks whether the top of the stack is a number (int or float).

is-list?:
Checks whether the top of the stack is a list.

is-string?:
Checks whether the top of the stack is a string.

is-bool?:
Checks whether the top of the stack is a boolean.

These commands help in writing conditional logic or debugging type issues in stack expressions.

6. Error Handling
Throughout the parser, assertions play a key role:

Stack Underflow:
Before performing operations that require one or more elements, the parser asserts the stack length is sufficient. If the stack is empty, an “EMPTY STACK” error is raised.
Invalid Operand Type:
Each operator checks that operands are of the expected type (e.g., number, list, boolean). If not, an "INVALID OPERAND TYPE" error is thrown.
Edge Conditions:
Division and exponentiation include checks such as division by zero and undefined negative exponent cases.
Errors are reported immediately to simplify debugging.

7. Extending the Language
Because Sanganak uses a token-based design with an extensible parser:

User-Defined Functions:
Functions can be added at runtime using def.
Global Variables:
Variables, stored in a global dictionary, allow persistent state between operations.
Custom Procedures:
The language design makes it straightforward to add new commands. You can modify the parser to interpret new tokens or constructs.

8. Example Programs
Simple Arithmetic
```
3 4 + put
```
Explanation:

Pushes 3 and 4 onto the stack.
+ pops them, computes 7, then pushes the result.
put prints the value.
List Creation and Iteration
```
1 2 3 list put
```
Explanation:

Pushes 1, 2, 3.
list aggregates the entire current stack into a single list.
put prints the list.
Conditional and Loops
```
true [ "Then branch executed" put ] [ "Else branch executed" put ] if
```
Explanation:

Pushes a boolean true and two procedures (the “then” and “else” parts).
The if command executes the corresponding procedure.
9. Conclusion
Sanganak is a minimal and expressive stack-based language that encourages programmers to think in terms of stack operations rather than named variables. The built-in operations cover arithmetic, I/O, list manipulations, and control flow. With support for user-defined functions and robust error handling, the language serves as both an educational tool and a foundation for more complex operations.

New users are encouraged to experiment with small snippets of code to become familiar with the stack model. The modular design of the lexer and parser also makes Sanganak ideal for extensions and further research.

10. Non-Allowed Keywords and Reserved Words
Sanganak reserves a set of keywords for its built-in operations. These keywords cannot be used by the programmer as the names of functions or variables. Attempting to redefine these may result in runtime exceptions or unexpected behavior. The reserved keywords include:

Stack Operations:
pop, dup, rot, concat

Arithmetic and Numeric Operations:
+, -, *, /, ^

Logical and Comparison Operators:
=, !=, <, >, <=, >=, not, and, or, xor,
b=, b!=, s=, s!=, lex>, lex<, lex>=, lex<=

I/O Operations:
get, put, print

Procedure Delimiters:
[, ], {, }

List Operations:
list, listn, spread, nth, len

Control Flow Keywords:
if, run, repeat, while, forever, foreach

Function Definition:
def

Increment/Decrement and Type Checking:
inc, dec, is-number?, is-list?, is-string?, is-bool?, is-symbol?, sym=

Boolean and Symbol Literals:
true, false

Important:
These keywords are hard-coded into the language's parser (parser.py) and lexer (lexer.py). They serve as the building blocks and control structure of the language. Any attempt to use these in user-defined names (via def) will lead to errors or may interfere with the normal execution of the parser. For instance, defining a function named + is not permitted because it overlaps with the built-in addition operator.

11. Language User Guide
Sanganak User Guide
Welcome to Sanganak! This guide is designed to help you quickly learn how to use Sanganak. It explains how to write programs, the meaning of various commands, and how to run and test your code.

Table of Contents
Getting Started
Writing Sanganak Programs
Stack Basics
Literals
Core Language Commands
Arithmetic Operations
Stack Manipulation
Input and Output
Control Flow: Conditionals and Loops
Defining Functions and Procedures
Reserved Keywords
Running and Debugging Programs
Example Programs
Tips and Best Practices
Further Resources
1. Getting Started
Sanganak is a stack-based programming language where every operation manipulates a common stack. Instead of named variables, your program works by pushing and popping values.

Installation & Setup:

Ensure you have installed Python (version 3.8+ recommended) on your Linux machine.

Clone your Sanganak repository and navigate to its root folder:

Your source code lives under the src folder and test files (if any) under directories like NewTests/.

2. Writing Sanganak Programs
Stack Basics
In Sanganak, a stack is a list where operations work on the most recent elements. Think of the stack as a pile of cards:

Push: Add a new card to the top.
Pop: Remove the top card.
Dup: Copy the top card.
Rot: Exchange the top two cards.
Literals
Write literal values directly; these include:

Numbers:
Write 42 or -7 for integers and 3.14 (or -0.5) for floats.

Strings:
Use double quotes to create a string. For example: "Hello, Sanganak!".

Booleans:
Use true and false (in lowercase) for boolean values.

Symbols:
Mark symbols with a preceding single quote, e.g. 'mySymbol.

3. Core Language Commands
Arithmetic Operations
You can perform basic arithmetic on numbers (which must already be on the stack):

Addition (+):
Push two numbers and then use + to add them.
Example:
10 5 +
Subtraction (-):
10 3 -   // Result: 7 (10 minus 3)
Multiplication (*):
4 6 *   // Result: 24
Division (/):
20 4 /   // Result: 5
Exponentiation (^):
2 3 ^   // Computes 2 raised to the power 3 -> 8
Stack Manipulation
Manage the order of your stack easily:

pop:
Removes the top element from the stack.

dup:
Duplicates the top stack element.

rot:
Reorders the top two elements (swaps them).

concat:
Pops two strings, concatenates them, and pushes the result.

Input and Output
Interact with the terminal using:

get:
Reads a value from the user at runtime.

put:
Prints the top element of the stack and removes it.
Example:
Write "Hello!" put to print Hello! with a new line.

print:
Similar to put but without extra formatting on strings.

Control Flow: Conditionals and Loops
Sanganak includes a set of commands to control the flow of your program.

Conditionals
Use the if command to choose between two code blocks:
true [ "Then branch" put ] [ "Else branch" put ] if
The first block executes if the condition is true; otherwise, the second block runs.
Loops
repeat:
5 [ "Hello" put ] repeat
Run a block a fixed number of times:
while:
Evaluates a condition and then runs a block repeatedly while the condition is true.
forever:
Begins an infinite loop until manually interrupted.
foreach:
Iterates over each element in a list and runs a procedure.
4. Defining Functions and Procedures
Procedures are groups of commands enclosed by [ ] or { }. They can be executed later using the run command.

To define a function, use the def command. For example:
'hello [ "Hello, World!" put ] def
This creates a function called hello that, when invoked, prints Hello, World!.

To invoke, simply call the function by its name (as a WordToken):
hello
5. Reserved Keywords
Certain keywords are reserved by Sanganak and cannot be redefined. These include:

Stack Operations: pop, dup, rot, concat
Arithmetic Operators: +, -, *, /, ^
Logical Operators: and, or, not, xor
Comparison and Boolean Operators: =, !=, <, >, <=, >=, b=, b!=, s=, s!=, lex>, lex<, lex>=, lex<=
I/O Operations: get, put, print
Code Block Delimiters: [, ], {, }
List Operations: list, listn, spread, nth, len
Control Flow: if, run, repeat, while, forever, foreach
Function Definition: def
Increment/Decrement and Type Checking: inc, dec, is-number?, is-list?, is-string?, is-bool?, is-symbol?, sym=
Literals for Boolean: true, false
Avoid using these words as names for your new functions or variables, as that will conflict with the language’s built-in operations.

6. Running and Debugging Programs
Running a Program
To run a Sanganak program:

Create a text file containing your Sanganak code. For example, create a file in the folder NewTests/ with your code.
Run the provided testing script. For example, use:
This script reads files from the NewTests/ folder, lexes them, and prints the tokens. Use it to verify the correctness of your program's syntax.

Debugging
Lexer Issues:
If your code isn’t lexed correctly, check your spacing around numbers, strings, or keywords.

Runtime Errors:
Look for messages like "EMPTY STACK" or "INVALID OPERAND TYPE". They indicate that an operation did not find the expected number of operands on the stack.

Testing Iteratively:
Write small snippets of code and test them with LexerTester.py or by directly running your program. This will help isolate issues due to incorrect token usage or faulty control flow.

7. Example Programs
Example 1: Basic Arithmetic
10 5 + put
Expected output: 15

Example 2: Combining Operations and Stack Manipulation
"Hello, " "World!" concat put
Expected output: "Hello, World!"

Example 3: Conditional Execution
false [ "This will not print" put ] [ "Else branch taken" put ] if
Expected output: Else branch taken

Example 4: Defining and Using a Custom Function
'echo [ dup put ] def  
"Test message" echo
Expected output: Test message

Example 5: Looping with repeat
3 [ "Loop iteration" put ] repeat
Expected output: Three lines, each with Loop iteration

8. Tips and Best Practices
Write Small:
Start with simple expressions to understand how the stack changes.

Comment Your Code:
Use comments (if supported externally, since Sanganak’s design is minimal) in your source files to document the purpose of code blocks.

Test Often:
Use the provided LexerTester.py to test changes. This helps catch syntax or lexing errors early.

Plan Your Stack:
Visualize your operations. Keep track of what your commands do on the stack—this is crucial when chaining multiple commands.

Respect Reserved Keywords:
Always check that new function names do not conflict with reserved keywords listed above.

9. Further Resources
Source Code:
Review the files in the src/ folder like lexer.py, parser.py, and astDefiner.py to understand the lower-level implementation (if interested).

Community Forums:
Join discussions or issue trackers related to Sanganak for help with advanced topics.

Experiment:
Modify and experiment with the runtime environment or add your own functions to fully grasp Sanganak’s extensibility.

Happy coding with Sanganak! Enjoy exploring the power of stack-based programming and building innovative solutions.

