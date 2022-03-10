"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

# to run from cmd: python SyntaxAnalser.py fibonacci.c

import sys, os

class FileParser:
    def __init__(self, filename):
        directory = os.path.dirname(__file__)
        self.filename = os.path.join(directory, filename)
        self.file = open(self.filename, "r")
        
    def __del__(self):
        self.file.close()
    
    def getNextCharacter(self):
        return self.file.read(1)

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

class SyntaxAnalyser:
    
    def __init__(self, filename):
        self.lexicalAnalyser = LexicalAnalyser(filename)
        self.token = self.lexicalAnalyser.getNextLexicalUnit()
        self.REL_OP = ["=", "<=", ">=", ">", "<", "<>"]
        self.ADD_OP = ["+", "-"]
        self.MUL_OP = ["*", "/"]

    def run(self): 
        self.__program()
        print("Compilation completed successfully")
    
    def __getNextToken(self):
        self.token = self.lexicalAnalyser.getNextLexicalUnit()

    def __program(self):
        if (self.token.lexicalUnit == "program"):
            
            self.__getNextToken()
            
            if (self.token.family == "identifier"):
            
                self.__getNextToken()
                
                self.__programBlock()
                
                if (self.token.lexicalUnit == "."):
                    
                    self.__getNextToken()
                    
                    if (self.token.lexicalUnit != ""):
                        print("No characters are allowed after the fullstop "
                              + "indicating the end of the program")
                        sys.exit()
                    
                else:
                    print("Every program should end with a fullstop, fullstop"
                           + " at the end is missing")
                    sys.exit()
                
            else:
                msg = ("The name of the program was expected after the keyword"
                       + " “program” in line 1. The illegal program name “" 
                       + self.token.lexicalUnit + "” appeared")
                print(msg)
                sys.exit()
        
        else:
            msg = ("keyword “program” expected in line 1. All programs " +  
            "should start with the keyword “program”. Ιnstead, the word " +
             self.token.lexicalUnit + " appeared")
            print(msg)
            sys.exit()
        
    def __programBlock(self):
        if (self.token.lexicalUnit == "{"):
            
            self.__getNextToken()
            
            self.__declarations()
            self.__subprograms()
            self.__blockstatements()
            
            if (self.token.lexicalUnit == "}"):
                self.__getNextToken()
            else:
                print("Expecting closing curly bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
            
        else:
            print("Expecting opening curly bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'") 
            sys.exit() 
                
    def __declarations(self):
        while (self.token.lexicalUnit == "declare"):
            self.__getNextToken()
            
            self.__varlist()
            
            if (self.token.lexicalUnit == ";"):
                self.__getNextToken()
            else:
                print("Expecting delimiter ';' at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
                
    def __varlist(self):
        if (self.token.family == "identifier"):
            self.__getNextToken()
          
            while(self.token.lexicalUnit == ","):
                self.__getNextToken()
                
                if (self.token.family == "identifier"):
                    self.__getNextToken()
                    
                else:
                    print("Expecting variable name at ({},{})"
                          .format(self.token.position[0], self.token.position[1])
                          + " instead received " + self.token.lexicalUnit)
                    sys.exit() 
            
        else:
            print("Expecting variable name at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received " + self.token.lexicalUnit) 
            sys.exit()      
            
    def __subprograms(self):
        while (self.token.lexicalUnit in ["function", "procedure"]):
            self.__getNextToken()
            self.__subprogram()

    def __subprogram(self):
        if (self.token.family == "identifier"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "("):
                self.__getNextToken()
                
                self.__formalparlist()
                
                if (self.token.lexicalUnit == ")"):
                    self.__getNextToken()
                    
                    self.__programBlock()
                
                else:
                    print("Expecting closing bracket at ({},{})"
                          .format(self.token.position[0], 
                                  self.token.position[1])
                          + " instead received '" + self.token.lexicalUnit + "'") 
                    sys.exit() 
            else:
                print("Expecting opening bracket at ({},{})"
                      .format(self.token.position[0], 
                              self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
        else:
            print("Expecting subprogram name at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'")
            sys.exit() 
    
    def __formalparlist(self):
        self.__formalparitem()
      
        while(self.token.lexicalUnit == ","):
            self.__getNextToken()
            
            self.__formalparitem()
                
    def __formalparitem(self):
        if (self.token.lexicalUnit in ["in", "inout"]):
            self.__getNextToken()
            
            if (self.token.family == "identifier"):
                self.__getNextToken()
            else:
                print("Expecting variable name at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'")
                sys.exit() 
        else:
            print("Expecting 'in' or 'inout' at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'")
            sys.exit() 
                
    def __statements(self):
        if (self.token.lexicalUnit == "{"):
            self.__getNextToken()
            
            self.__statement()
            
            while(self.token.lexicalUnit == ";"):
                self.__getNextToken()
                
                self.__statement()
                
            if (self.token.lexicalUnit == "}"):
                self.__getNextToken()
            else:
                print("Expecting closing curly bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
        else:
            self.__statement()
            
            if (self.token.lexicalUnit == ";"):
                self.__getNextToken()
            else:
                print("Expecting delimiter ';' at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
                
    def __blockstatements(self):
        self.__statement()
        
        while(self.token.lexicalUnit == ";"):
            self.__getNextToken()
            
            self.__statement()
            
    
    def __statement(self):
        
        if (self.token.family == "identifier"):
            self.__getNextToken()
            self.__assignStat()
        elif (self.token.lexicalUnit == "if"):
            self.__getNextToken()
            self.__ifStat()
        elif (self.token.lexicalUnit == "while"):
            self.__getNextToken()
            self.__whileStat()
        elif (self.token.lexicalUnit == "switchcase"):
            self.__getNextToken()
            self.__switchcaseStat()
        elif (self.token.lexicalUnit == "forcase"):
            self.__getNextToken()
            self.__forcaseStat()
        elif (self.token.lexicalUnit == "incase"):
            self.__getNextToken()
            self.__incaseStat()
        elif (self.token.lexicalUnit == "call"):
            self.__getNextToken()
            self.__callStat()      
        elif (self.token.lexicalUnit == "return"):
            self.__getNextToken()
            self.__returnStat()
        elif (self.token.lexicalUnit == "input"):
            self.__getNextToken()
            self.__inputStat()           
        elif (self.token.lexicalUnit == "print"):
            self.__getNextToken()
            self.__printStat()
            
    def __assignStat(self):
        if (self.token.lexicalUnit == ":="):
            self.__getNextToken()
            
            self.__expression()
        
        else:
            print("Expecting assign symbol ':=' at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'") 
            sys.exit() 

    def __ifStat(self):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            self.__condition()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
                
                self.__statements()
                self.__elsepart()
            else:
                print("Expecting closing bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
        else:
            print("Expecting opening bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'") 
            sys.exit()

    def __elsepart(self):
        if (self.token.lexicalUnit == "else"):
           self.__getNextToken()
           
           self.__statements()
           
    def __whileStat(self):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            self.__condition()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
                
                self.__statements()
            else:
                print("Expecting closing bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
        else:
            print("Expecting opening bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'") 
            sys.exit()

    def __switchcaseStat(self):
        while (self.token.lexicalUnit == "case"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "("):
                self.__getNextToken()
                
                self.__condition()
                
                if (self.token.lexicalUnit == ")"):
                    self.__getNextToken()
                    
                    self.__statements()
                else:
                    print("Expecting closing bracket at ({},{})"
                          .format(self.token.position[0], self.token.position[1])
                          + " instead received '" + self.token.lexicalUnit + "'") 
                    sys.exit() 
            else:
                print("Expecting opening bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit()
            
        if (self.token.lexicalUnit == "default"):
            self.__getNextToken()
            
            self.__statements()
        else:
            print("Expecting default at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'") 
            sys.exit() 

    def __forcaseStat(self):
        while (self.token.lexicalUnit == "case"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "("):
                self.__getNextToken()
                
                self.__condition()
                
                if (self.token.lexicalUnit == ")"):
                    self.__getNextToken()
                    
                    self.__statements()
                else:
                    print("Expecting closing bracket at ({},{})"
                          .format(self.token.position[0], self.token.position[1])
                          + " instead received '" + self.token.lexicalUnit + "'") 
                    sys.exit() 
            else:
                print("Expecting opening bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit()
            
        if (self.token.lexicalUnit == "default"):
            self.__getNextToken()
            
            self.__statements()
        else:
            print("Expecting default at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'") 
            sys.exit() 
            
    def __incaseStat(self):
        while (self.token.lexicalUnit == "case"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "("):
                self.__getNextToken()
                
                self.__condition()
                
                if (self.token.lexicalUnit == ")"):
                    self.__getNextToken()
                    
                    self.__statements()
                else:
                    print("Expecting closing bracket at ({},{})"
                          .format(self.token.position[0], self.token.position[1])
                          + " instead received '" + self.token.lexicalUnit + "'") 
                    sys.exit() 
            else:
                print("Expecting opening bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit()
                
    def __returnStat(self):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            self.__expression()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
                
            else:
                print("Expecting closing bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
        else:
            print("Expecting opening bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'") 
            sys.exit()
            
    def __callStat(self):
        if (self.token.family == "identifier"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "("):
                self.__getNextToken()
                
                self.__actualparlist()
                
                if (self.token.lexicalUnit == ")"):
                    self.__getNextToken()
                else:
                    print("Expecting closing bracket at ({},{})"
                          .format(self.token.position[0], self.token.position[1])
                          + " instead received '" + self.token.lexicalUnit + "'") 
                    sys.exit() 
            else:
                print("Expecting opening bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit()
        else:
            print("Expecting variable name at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'")
            sys.exit()
            
    def __printStat(self):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            self.__expression()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
                
            else:
                print("Expecting closing bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
        else:
            print("Expecting opening bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'") 
            sys.exit()
            
    def __inputStat(self):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            if (self.token.family == "identifier"):
                self.__getNextToken()
            else:
                print("Expecting variable name at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'")
                sys.exit()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
            else:
                print("Expecting closing bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
        else:
            print("Expecting opening bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'") 
            sys.exit()
            
    def __actualparlist(self):     
        self.__actualparitem()
    
        while (self.token.lexicalUnit == ","):
            self.__getNextToken()
            
            self.__actualparitem()
                
    def __actualparitem(self):
        if (self.token.lexicalUnit == "in"):
            self.__getNextToken()
            self.__expression()
        
        elif (self.token.lexicalUnit == "inout"):
            self.__getNextToken()
            if (self.token.family == "identifier"):
                self.__getNextToken()
        
        else:
            print("Expecting 'in' or 'inout' at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'")
            sys.exit() 
            
    def __condition(self):
        self.__boolterm()
        
        while (self.token.lexicalUnit == "or"):
            self.__getNextToken()
            
            self.__boolterm()
            
    def __boolterm(self):
        self.__boolfactor()
        
        while (self.token.lexicalUnit == "and"):
            self.__getNextToken()
            
            self.__boolfactor()
            
    def __boolfactor(self):
        
        if (self.token.lexicalUnit == "not"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "["):
                self.__getNextToken()
                
                self.__condition()
                
                if (self.token.lexicalUnit == "]"):
                    self.__getNextToken()
                else:
                    print("Expecting closeing square bracket at ({},{})"
                          .format(self.token.position[0], 
                                  self.token.position[1])
                          + " instead received '" + self.token.lexicalUnit + "'") 
                    sys.exit() 
                
            else:
                print("Expecting opening square bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
        
        elif (self.token.lexicalUnit == "["):
            self.__getNextToken()
            
            self.__condition()

            if (self.token.lexicalUnit == "]"):
                self.__getNextToken()
            else:
                print("Expecting closeing square bracket at ({},{})"
                      .format(self.token.position[0], 
                              self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
        
        else:
            self.__expression()
            
            if (self.token.lexicalUnit in self.REL_OP):
                self.__getNextToken()
            else:
                print("Expecting relational operator at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'")
                sys.exit()
        
            self.__expression()

    def __expression(self):
        self.__optionalSign()
        self.__term()
        
        while (self.token.lexicalUnit in self.ADD_OP):
            self.__getNextToken()
            
            self.__term()
    
    def __term(self):
        self.__factor()
        
        while (self.token.lexicalUnit in self.MUL_OP):
            self.__getNextToken()
            
            self.__factor()

    def __factor(self):
        if (self.token.family == "number"):
            self.__getNextToken()
        
        elif (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            self.__expression()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
            else:
                print("Expecting closing bracket at ({},{})"
                      .format(self.token.position[0], 
                              self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit()
        
        elif (self.token.family == "identifier"):
            self.__getNextToken()
            
            self.__idtail()
        
        else:
            print("Received invalid symbol {} at ({},{})"
                  .format(self.token.lexicalUnit, self.token.position[0], 
                          self.token.position[1])) 
            sys.exit()
            
    def __idtail(self):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            self.__actualparlist()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
            else:
                print("Expecting closeing bracket at ({},{})"
                      .format(self.token.position[0], 
                              self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit()
                
    def __optionalSign(self):
        if (self.token.lexicalUnit in self.ADD_OP):
            self.__getNextToken()
    

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Wrong arguments. Must give just the filename")
        sys.exit()

    filename = sys.argv[1]
    
    syntaxAnalyser = SyntaxAnalyser(filename)
    syntaxAnalyser.run()