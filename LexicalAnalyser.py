"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

import sys
from FileParser import FileParser

class Token:
    
    def __init__(self, lexicalUnit, family, position):
        self.lexicalUnit = lexicalUnit
        self.family = family
        self.position = position

class LexicalAnalyser:
    
    def __init__(self, filename):
        self.fileParser = FileParser(filename)
        self.nextChar = " "
        self.lexicalUnit = ""
        self.state = "start"
        self.row = 1
        self.col = 1
        self.nextRow = 1
        self.nextCol = 1
        self.ignoreSymbols = [" ", "\t", "\n"]
        self.states = [['start', 'idk', 'dig', 'addOperator', 'mulOperator',
                        'groupSymbol', 'delimiter', 'asgn', 'smaller',
                        'larger', 'relOperator', 'rem', 'eof', 'error'],
                       ['id/key', 'idk', 'idk', 'id/key', 'id/key', 'id/key',
                        'id/key', 'id/key', 'id/key', 'id/key', 'id/key',
                        'id/key', 'id/key', 'id/key'],
                       ['number', 'error', 'dig', 'number', 'number', 'number',
                        'number', 'number', 'number', 'number', 'number',
                        'number', 'number', 'number'],
                       ['error', 'error', 'error', 'error', 'error', 'error',
                        'error', 'error', 'error', 'error', 'assignment',
                        'error', 'error', 'error'],
                       ['relOperatorBt', 'relOperatorBt', 'relOperatorBt',
                        'relOperatorBt', 'relOperatorBt', 'relOperatorBt',
                        'relOperatorBt', 'relOperatorBt', 'relOperatorBt',
                        'relOperator', 'relOperator', 'relOperatorBt',
                        'relOperatorBt', 'relOperatorBt'],
                       ['relOperatorBt', 'relOperatorBt', 'relOperatorBt',
                        'relOperatorBt', 'relOperatorBt', 'relOperatorBt',
                        'relOperatorBt', 'relOperatorBt', 'relOperatorBt',
                        'relOperatorBt', 'relOperator', 'relOperatorBt',
                        'relOperatorBt', 'relOperatorBt'],
                       ['rem', 'rem', 'rem', 'rem', 'rem', 'rem', 'rem', 'rem',
                        'rem', 'rem', 'rem', 'start', 'error', 'rem'] ]
        self.internalState = {'start' : 0, 'idk' : 1, 'dig' : 2, 'asgn' : 3,
                              'smaller' : 4, 'larger' : 5, 'rem' : 6}
        self.reservedWords = ["program", "declare", "if", "else",  "while",
                              "switchcase", "forcase", "incase", "case",
                              "default", "not", "and", "or", "function",
                              "procedure", "call", "return", "in", "inout", 
                              "input", "print"]
        
    """
    Returns the lexical unit token to the syntax analyser.
    According to the current state it consumes the next char or not.
    """
    def getNextLexicalUnit(self):
        
        self.state = "start"
        self.lexicalUnit = ""
        self.row = self.nextRow
        self.col = self.nextCol
        
        while True:
            
            previousState = self.state
            
            # Get state array index accoding to next input character
            inputVal = self.__getNextInputIndex(self.nextChar)
                
            # find next state from table of states
            self.state = self.states[self.internalState[self.state]][inputVal]
            
            # Take action according to state
            if (self.state in ["start", "rem"]):
                self.nextChar = self.__nextChar()
            
            elif (self.state in ["idk", "dig", "asgn", "smaller", "larger"]):
                self.lexicalUnit += self.nextChar
                self.nextChar = self.__nextChar()
            
            elif (self.state == "id/key"):
                # check for lexical units with more than 30 characters
                if (len(self.lexicalUnit) > 30):
                    msg = " Lexical unit is more than 30 characters long"
                    error = ("LexError at {}.".format((self.row, self.col)) 
                             + msg)
                    # return Token(error, "error", (self.row, self.col))
                    print(error)
                    sys.exit()
                
                if (self.lexicalUnit in self.reservedWords):
                    return Token(self.lexicalUnit, "keyword", 
                                 (self.row, self.col))
                else:
                    return Token(self.lexicalUnit, "identifier", 
                                 (self.row, self.col))
            
            elif (self.state == "number"):
                # check for numbers < -2^32-1 or > 2^32-1
                if (abs(int(self.lexicalUnit)) > 4294967295):
                    msg = " Number exceeds maximum supported"
                    error = ("LexError at {}.".format((self.row, self.col)) 
                             + msg)
                    # return Token(error, "error", (self.row, self.col))
                    print(error)
                    sys.exit()
                
                return Token(self.lexicalUnit, self.state, 
                             (self.row, self.col))
           
            elif (self.state in ["addOperator", "mulOperator", "groupSymbol",
                                 "delimiter", "assignment", "relOperator",
                                 "eof"]):
                # if (self.nextChar == ""): 
                #     return
                self.lexicalUnit += self.nextChar
                self.nextChar = self.__nextChar()
                return Token(self.lexicalUnit, self.state, (self.row, self.col))
           
            elif (self.state == "relOperatorBt"):
                return Token(self.lexicalUnit, "relOperator", 
                             (self.row, self.col))
            
            elif (self.state == "error"):
                msg = self.__getErrorMessage(previousState)   
                error = ("LexError at {}.".format((self.row, self.col)) + msg)
                # return Token(error, self.state, (self.row, self.col))
                print(error)
                sys.exit()

    def __getNextInputIndex(self, char):
        
           if (char in self.ignoreSymbols):
               return 0
           elif (char.isalpha()):
               return 1
           elif (char.isdigit()):
               return 2
           elif (char in ["+", "-"]):
               return 3
           elif (char in ["*", "/"]):
               return 4
           elif (char in ["{", "}", "[", "]", "(", ")"]):
               return 5
           elif (char in [",", ";", "."]):
               return 6
           elif (char == ":"):
               return 7
           elif (char == "<"):
               return 8
           elif (char == ">"):
               return 9
           elif (char == "="):
               return 10
           elif (char == "#"):
               return 11
           elif (char == ""):   # EOF
               return 12
           else:
               return 13
        
    def __nextChar(self):
        
        # keep track of row/column number for error message
        if (self.nextChar == "\n"):
            self.nextRow += 1
            self.nextCol = 0
        elif (self.nextChar == "\t"):
            self.nextCol += 4
        else:
            self.nextCol += 1
        
        return self.fileParser.getNextCharacter()      
    
    def __getErrorMessage(self, previousState):
        if (previousState == "start"):
            return " Character not supported"
        elif (previousState == "dig"):
            return " Alphanumeric character in digit"
        elif (previousState == "asgn"):
            return" Illegal character after : Expected ="
        elif (previousState == "rem"):
            return " Comment block closing sign (#) missing"


###############################################################################
#################                   T E S T S                 #################
###############################################################################

def test_countDigits():
    
    # fileParser = FileParser("countDigits.c")
    lexicalAnalyser = LexicalAnalyser("countDigits.c")
    
    correctWords = ['program', 'countDigits', '{', 'declare', 'x', ',',
                    'count', ';', 'input', '(', 'x', ')', ';', 'count', ':=',
                    '0', ';', 'while', '(', 'x', '>', '0', ')', '{', 'x', ':=',
                    'x', '/', '10', ';', 'count', ':=', 'count', '+', '1', ';',
                    '}', ';', 'print', '(', 'count', ')', ';', '}', '.']

    i = 0
    nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit().lexicalUnit
    while (nextLexicalUnit != "."):
        
        # print(nextLexicalUnit)
        # print(correctWords[i])
        assert nextLexicalUnit == correctWords[i], nextLexicalUnit
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit().lexicalUnit
        i += 1
    
    # print(nextLexicalUnit)
    assert nextLexicalUnit == correctWords[i], nextLexicalUnit
    
    print("Test case countDigits.c: Everything passed")

def test_factorial():
    
    # fileParser = FileParser("factorial.c")
    lexicalAnalyser = LexicalAnalyser("factorial.c")
    
    correctWords = ['program', 'factorial', '{', 'declare', 'x', ';',
                    'declare', 'i', ',', 'fact', ';', 'input', '(', 'x', ')',
                    ';', 'fact', ':=', '1', ';', 'i', ':=', '1', ';', 'while',
                    '(', 'i', '<=', 'x', ')', '{', 'fact', ':=', 'fact',
                    '*', 'i', ';', 'i', ':=', 'i', '+', '1', ';', '}', ';',
                    'print', '(', 'fact', ')', ';', '}', '.']

    i = 0
    nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit().lexicalUnit
    while (nextLexicalUnit != "."):
        
        # print(nextLexicalUnit)
        # print(correctWords[i])
        assert nextLexicalUnit == correctWords[i], nextLexicalUnit
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit().lexicalUnit
        i += 1
    
    # print(nextLexicalUnit)
    assert nextLexicalUnit == correctWords[i], nextLexicalUnit
    
    print("Test case factorial.c: Everything passed")
    
def test_fibonacci():
    
    # fileParser = FileParser("fibonacci.c")
    lexicalAnalyser = LexicalAnalyser("fibonacci.c")
    
    correctWords = ['program', 'fibonacci', '{', 'declare', 'x', ';', 
                    'function', 'fibonacci', '(', 'in', 'x', ')', '{', 
                    'return', '(', 'fibonacci', '(', 'in', 'x', '-', '1', ')', 
                    '+', 'fibonacci', '(', 'in', 'x', '-', '2', ')', ')', ';',
                    '}', 'input', '(', 'x', ')', ';', 'print', '(', 
                    'fibonacci', '(', 'in', 'x', ')', ')', ';', '}', '.']

    i = 0
    nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit().lexicalUnit
    while (nextLexicalUnit != "."):
        
        # print(nextLexicalUnit)
        # print(correctWords[i])
        assert nextLexicalUnit == correctWords[i], nextLexicalUnit
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit().lexicalUnit
        i += 1
    
    # print(nextLexicalUnit)
    assert nextLexicalUnit == correctWords[i], nextLexicalUnit
    
    print("Test case factorial.c: Everything passed")
      
def test_primes():
    
    # fileParser = FileParser("primes.c")
    lexicalAnalyser = LexicalAnalyser("primes.c")
    
    correctWords = ['program', 'primes', '{', 'declare', 'i', ';', 'function',
                    'isPrime', '(', 'in', 'x', ')', '{', 'declare', 'i', ';',
                    'function', 'divides', '(', 'in', 'x', ',', 'in', 'y', ')',
                    '{', 'if', '(', 'y', '=', '(', 'y', '/', 'x', ')', '*',
                    'x', ')', 'return', '(', '1', ')', ';', 'else', 'return',
                    '(', '0', ')', ';', '}', 'i', ':=', '2', ';', 'while', '(',
                    'i', '<', 'x', ')', '{', 'if', '(', 'divides', '(', 'in',
                    'i', ',', 'in', 'x', ')', '=', '1', ')', 'return', '(',
                    '0', ')', ';', ';', 'i', ':=', 'i', '+', '1', '}', ';',
                    'return', '(', '1', ')', '}', 'i', ':=', '2', ';', 'while',
                    '(', 'i', '<=', '30', ')', 'if', '(', 'isPrime', '(',
                    'in', 'i', ')', '=', '1', ')', 'print', '(', 'i', ')', ';',
                    ';', '}', '.']

    i = 0
    nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit().lexicalUnit
    while (nextLexicalUnit != "."):
        
        # print(nextLexicalUnit)
        # print(correctWords[i])
        assert nextLexicalUnit == correctWords[i], nextLexicalUnit
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit().lexicalUnit
        i += 1
    
    # print(nextLexicalUnit)
    assert nextLexicalUnit == correctWords[i], nextLexicalUnit
    
    print("Test case primes.c: Everything passed")
        
def test_summation():
    
    # fileParser = FileParser("summation.c")
    lexicalAnalyser = LexicalAnalyser("summation.c")
    
    correctWords = ['program', 'summation', '{', 'declare', 'x', ',', 'sum',
                    ';', 'input', '(', 'x', ')', ';', 'sum', ':=', '0', ';',
                    'forcase', 'case', '(', 'x', '>', '0', ')', '{', 'sum',
                    ':=', 'sum', '+', 'x', ';', 'x', ':=', 'x', '-', '1', ';',
                    '}', 'default', 'print', '(', 'sum', ')', ';', '}', '.']

    i = 0
    nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit().lexicalUnit
    while (nextLexicalUnit != "."):
        
        # print(nextLexicalUnit)
        # print(correctWords[i])
        assert nextLexicalUnit == correctWords[i], nextLexicalUnit
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit().lexicalUnit
        i += 1
    
    # print(nextLexicalUnit)
    assert nextLexicalUnit == correctWords[i], nextLexicalUnit
    
    print("Test case summation.c: Everything passed")   
      

if __name__ == "__main__":
    
    automaticTesting = True
    manualTesting = True
    
    if automaticTesting:
        test_countDigits()
        test_factorial()
        test_fibonacci()
        test_primes()
        test_summation()
    
    if manualTesting:
               
        lexicalAnalyser = LexicalAnalyser("factorial.c")
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
        while (nextLexicalUnit.lexicalUnit != "."):
            
            if (nextLexicalUnit.lexicalUnit.startswith("LexError")):
                break
    
            print("{}\t\t\t family: {},\t position: {}"
                  .format(nextLexicalUnit.lexicalUnit, nextLexicalUnit.family,
                          nextLexicalUnit.position))        
            
            nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
        
        print("{}\t family: {},\t position: {}"
              .format(nextLexicalUnit.lexicalUnit, nextLexicalUnit.family,
                      nextLexicalUnit.position))