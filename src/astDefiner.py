from dataclasses import dataclass

class AST: # Abstract Syntax Tree
    pass

@dataclass
class Number(AST): # Number class
    val: str

@dataclass
class DecimalNumber(AST): # Decimal Number class
    val: str

@dataclass
class NegNumber(AST): # Negative Number class
    val: str

@dataclass
class NegDecimalNumber(AST): # Negative Decimal Number class
    val: str

@dataclass
class Word(AST): # Word class
    val: str

@dataclass
class String(AST): # String class
    val: str

@dataclass
class Bools(AST): # Bool
    val: str