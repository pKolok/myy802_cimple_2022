"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

class LexicalAnalyser:
    def __init__(self, fileParser):
        self.fileParser = fileParser
        self.nextChar = " "
        self.row = 1
        self.col = 0
        self.ignoreSymbols = [" ", "\t", "\n"]
        self.selfStandingSymbols = ["+", "-", "*", "/", "=", ",", ";", ")", 
                                    "(", "[", "]", "{", "}", ".", ""]
        
    def getNextLexicalUnit(self):
        
        lexicalUnit = ""
        # char = self.__nextChar()
        char = self.nextChar
        
        # White character -> stay in state 0
        while (char in self.ignoreSymbols):
            char = self.__nextChar()
        
        # Comments -> go to state 6
        if (char == "#"):
            char = self.__nextChar()
            while (char != "#"):
                if (char == ""):    # EOF
                    return ("LexError at ({},{}) - Unexpected End Of File (EOF)"
                            .format(self.row, self.col))
                char = self.__nextChar()
            
            char = self.__nextChar()
            while (char in self.ignoreSymbols):
                char = self.__nextChar()
        
        # Alphanumerical -> go to state 1
        if (char.isalpha()):
            lexicalUnit += char
            char = self.__nextChar()
            while (char.isalpha() or char.isdigit()):
                lexicalUnit += char
                char = self.__nextChar()
            
            self.nextChar = char
            return lexicalUnit
    
        # Digit -> go to state 2
        if (char.isdigit()):
            lexicalUnit += char
            char = self.__nextChar()
            while (char.isdigit()):
                lexicalUnit += char
                char = self.__nextChar()
            
            self.nextChar = char
            return lexicalUnit
            
        # Less-than (<) -> go to state 3
        if (char == "<"):
            lexicalUnit += char
            char = self.__nextChar()
            if (char == "=" or char == ">"):
                lexicalUnit += char
                self.nextChar = self.__nextChar()
                return lexicalUnit
            else:
                self.nextChar = char
                return lexicalUnit
    
        # Greater-than (>) -> go to state 4
        if (char == ">"):
            lexicalUnit += char
            char = self.__nextChar()
            if (char == "="):
                lexicalUnit += char
                self.nextChar = self.__nextChar()
                return lexicalUnit
            else:
                self.nextChar = char
                return lexicalUnit
            
        # Colon (>) -> go to state 5
        if (char == ":"):
            lexicalUnit += char
            char = self.__nextChar()
            if (char == "="):
                lexicalUnit += char
                self.nextChar = self.__nextChar()
                return lexicalUnit
            else:
                return ("LexError at ({},{}) - expected '=' sign after ':' sign"
                        .format(self.row, self.col))
    
        # Language recognised self-standing symbols
        if (char in self.selfStandingSymbols):
            lexicalUnit += char
            self.nextChar = self.__nextChar()
            return lexicalUnit
        
        # If none of the above -> not a language character
        # self.nextChar = self.__nextChar()
        return ("LexError at ({},{}) - Unrecognised character: {}"
                .format(self.row, self.col, char))
    
    
    def __nextChar(self):
        char = self.fileParser.getNextCharacter()
        
        # keep track of row/column number for error message
        self.col += 1
        if (char == "\n"):
            self.row += 1
            self.col = 0
        
        return char   


###############################################################################
#################                   T E S T S                 #################
###############################################################################

def test_countDigits():
    
    fileParser = FileParser("countDigits.c")
    lexicalAnalyser = LexicalAnalyser(fileParser)
    
    correctWords = ['program', 'countDigits', '{', 'declare', 'x', ',',
                    'count', ';', 'input', '(', 'x', ')', ';', 'count', ':=',
                    '0', ';', 'while', '(', 'x', '>', '0', ')', '{', 'x', ':=',
                    'x', '/', '10', ';', 'count', ':=', 'count', '+', '1', ';',
                    '}', ';', 'print', '(', 'count', ')', ';', '}', '.']

    i = 0
    nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
    while (nextLexicalUnit != "."):
        
        # print(nextLexicalUnit)
        # print(correctWords[i])
        assert nextLexicalUnit == correctWords[i], nextLexicalUnit
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
        i += 1
    
    # print(nextLexicalUnit)
    assert nextLexicalUnit == correctWords[i], nextLexicalUnit
    
    print("Test case countDigits.c: Everything passed")

def test_factorial():
    
    fileParser = FileParser("factorial.c")
    lexicalAnalyser = LexicalAnalyser(fileParser)
    
    correctWords = ['program', 'factorial', '{', 'declare', 'x', ';',
                    'declare', 'i', ',', 'fact', ';', 'input', '(', 'x', ')',
                    ';', 'fact', ':=', '1', ';', 'i', ':=', '1', ';', 'while',
                    '(', 'i', '<=', 'x', ')', '{', 'fact', ':=', 'fact',
                    '*', 'i', ';', 'i', ':=', 'i', '+', '1', ';', '}', ';',
                    'print', '(', 'fact', ')', ';', '}', '.']

    i = 0
    nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
    while (nextLexicalUnit != "."):
        
        # print(nextLexicalUnit)
        # print(correctWords[i])
        assert nextLexicalUnit == correctWords[i], nextLexicalUnit
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
        i += 1
    
    # print(nextLexicalUnit)
    assert nextLexicalUnit == correctWords[i], nextLexicalUnit
    
    print("Test case factorial.c: Everything passed")
    
def test_fibonacci():
    
    fileParser = FileParser("fibonacci.c")
    lexicalAnalyser = LexicalAnalyser(fileParser)
    
    correctWords = ['program', 'fibonacci', '{', 'declare', 'x', ';', 
                    'function', 'fibonacci', '(', 'in', 'x', ')', '{', 
                    'return', '(', 'fibonacci', '(', 'in', 'x', '-', '1', ')', 
                    '+', 'fibonacci', '(', 'in', 'x', '-', '2', ')', ')', ';',
                    '}', 'input', '(', 'x', ')', ';', 'print', '(', 
                    'fibonacci', '(', 'in', 'x', ')', ')', ';', '}', '.']

    i = 0
    nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
    while (nextLexicalUnit != "."):
        
        # print(nextLexicalUnit)
        # print(correctWords[i])
        assert nextLexicalUnit == correctWords[i], nextLexicalUnit
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
        i += 1
    
    # print(nextLexicalUnit)
    assert nextLexicalUnit == correctWords[i], nextLexicalUnit
    
    print("Test case factorial.c: Everything passed")
      
def test_primes():
    
    fileParser = FileParser("primes.c")
    lexicalAnalyser = LexicalAnalyser(fileParser)
    
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
    nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
    while (nextLexicalUnit != "."):
        
        # print(nextLexicalUnit)
        # print(correctWords[i])
        assert nextLexicalUnit == correctWords[i], nextLexicalUnit
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
        i += 1
    
    # print(nextLexicalUnit)
    assert nextLexicalUnit == correctWords[i], nextLexicalUnit
    
    print("Test case primes.c: Everything passed")
        
def test_summation():
    
    fileParser = FileParser("summation.c")
    lexicalAnalyser = LexicalAnalyser(fileParser)
    
    correctWords = ['program', 'summation', '{', 'declare', 'x', ',', 'sum',
                    ';', 'input', '(', 'x', ')', ';', 'sum', ':=', '0', ';',
                    'forcase', 'case', '(', 'x', '>', '0', ')', '{', 'sum',
                    ':=', 'sum', '+', 'x', ';', 'x', ':=', 'x', '-', '1', ';',
                    '}', 'default', 'print', '(', 'sum', ')', ';', '}', '.']

    i = 0
    nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
    while (nextLexicalUnit != "."):
        
        # print(nextLexicalUnit)
        # print(correctWords[i])
        assert nextLexicalUnit == correctWords[i], nextLexicalUnit
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
        i += 1
    
    # print(nextLexicalUnit)
    assert nextLexicalUnit == correctWords[i], nextLexicalUnit
    
    print("Test case summation.c: Everything passed")    
    

if __name__ == "__main__":
    
    from FileParser import FileParser
    
    manualTesting = False
    
    test_countDigits()
    test_factorial()
    test_fibonacci()
    test_primes()
    test_summation()

    if (manualTesting):
        
        filename = ("summation.c")
        fileParser = FileParser(filename)
        
        lexicalAnalyser = LexicalAnalyser(fileParser)
        
        nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
        while (nextLexicalUnit != "."):
            
            if (nextLexicalUnit.startswith("LexError")):
                break
    
            print(nextLexicalUnit)        
            
            nextLexicalUnit = lexicalAnalyser.getNextLexicalUnit()
        
        print(nextLexicalUnit)
    # end of manual testing