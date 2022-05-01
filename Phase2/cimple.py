"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

# to run from cmd: python3 cimple.py fibonacci.c

import os
import sys
from abc import ABC

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
        self.filename = filename
        self.lexicalAnalyser = LexicalAnalyser(filename)
        self.token = self.lexicalAnalyser.getNextLexicalUnit()
        self.REL_OP = ["=", "<=", ">=", ">", "<", "<>"]
        self.ADD_OP = ["+", "-"]
        self.MUL_OP = ["*", "/"]
        self.intermediateCode = IntermediateCode()
        self.symbolsTable = SymbolsTable()

    def run(self): 
        self.__program()
        print("Compilation completed successfully (" + self.filename + ")")
        print("--------------------------------------")
        print(">>> Intermediate Code: <<<")
        self.intermediateCode.printOut()
        self.intermediateCode.saveToFile()
        self.intermediateCode.convertToC()
        print("--------------------------------------")
        print(">>> Scope trace: <<<")
        self.symbolsTable.printScopeTrace()
        self.symbolsTable.saveScopeTraceToFile()
        print("--------------------------------------")
    
    def __getNextToken(self):
        self.token = self.lexicalAnalyser.getNextLexicalUnit()

    def __program(self):
        if (self.token.lexicalUnit == "program"):
            
            self.__getNextToken()
            
            # Symbols table
            self.symbolsTable.addScope("main")
            
            if (self.token.family == "identifier"):
                name = self.token.lexicalUnit
            
                self.__getNextToken()

                self.__programBlock(name)
                
                self.intermediateCode.genQuad("halt", "_", "_", "_")
                self.intermediateCode.genQuad("end_block", name, "_", "_")

                # Symbols table
                frameLength = self.symbolsTable.getTopScopeSize()
                self.symbolsTable.saveScopeString()
                self.symbolsTable.removeLastScope()
                self.symbolsTable.setMainFrameLength(frameLength)

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
                       + " \"program\" in line 1. The illegal program name \"" 
                       + self.token.lexicalUnit + "\" appeared")
                print(msg)
                sys.exit()
        
        else:
            msg = ("keyword \"program\" expected in line 1. All programs " +  
            "should start with the keyword \"program\". Instead, the word " +
             self.token.lexicalUnit + " appeared")
            print(msg)
            sys.exit()
        
    def __programBlock(self, name):
        if (self.token.lexicalUnit == "{"):
            self.__getNextToken()
            
            self.__declarations()
            self.__subprograms()
            
            self.intermediateCode.genQuad("begin_block", name, "_", "_")
            
            # Symbols Table
            self.symbolsTable.fillInStartingQuad(self.intermediateCode
                                                 .nextQuad())
            
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
            
            # Symbols Table
            self.symbolsTable.addVariable(self.token.lexicalUnit)
            
            self.__getNextToken()
          
            while(self.token.lexicalUnit == ","):
                self.__getNextToken()
                
                if (self.token.family == "identifier"):
                    
                    # Symbols Table
                    self.symbolsTable.addVariable(self.token.lexicalUnit)
                    
                    self.__getNextToken()
                    
                else:
                    print("Expecting variable name at ({},{})"
                          .format(self.token.position[0], self.token.position[1])
                          + " instead received " + self.token.lexicalUnit)
                    sys.exit()
            
    def __subprograms(self):
        while (self.token.lexicalUnit in ["function", "procedure"]):
            
            # Symbols Table
            # Add function to current scope
            if (self.token.lexicalUnit == "function"):
                self.__getNextToken()
                name = self.token.lexicalUnit
                self.symbolsTable.addFunction(name, "int")
            # Add procedure to current scope
            else:
                self.__getNextToken()
                name = self.token.lexicalUnit
                self.symbolsTable.addProcedure(name)
            
            # Symbols Table
            self.symbolsTable.addScope(name)
            
            self.__subprogram(name)
            
            # Symbols Table
            frameLength = self.symbolsTable.getTopScopeSize()
            self.symbolsTable.saveScopeString()
            self.symbolsTable.removeLastScope()
            self.symbolsTable.fillInFrameLength(frameLength)
            
            self.intermediateCode.genQuad("end_block", name, "_", "_")

    def __subprogram(self, name):
        if (self.token.family == "identifier"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "("):
                self.__getNextToken()
                
                self.__formalparlist()
                
                if (self.token.lexicalUnit == ")"):
                    self.__getNextToken()
                    
                    self.__programBlock(name)
                
                else:
                    print("Expecting closing bracket at ({},{})"
                          .format(self.token.position[0], 
                                  self.token.position[1])
                          + " instead received '" + self.token.lexicalUnit 
                          + "'") 
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
        if (self.token.lexicalUnit in ["in", "inout"]):
            self.__formalparitem()
          
            while(self.token.lexicalUnit == ","):
                self.__getNextToken()
                
                self.__formalparitem()
                
    def __formalparitem(self):
        if (self.token.lexicalUnit in ["in", "inout"]):
            
            # Symbols Table
            mode = "cv" if self.token.lexicalUnit == "in" else "ref"
            
            self.__getNextToken()
            
            if (self.token.family == "identifier"):
                
                # Symbols Table
                name = self.token.lexicalUnit
                self.symbolsTable.addParameter(name, "int", mode)
                self.symbolsTable.appendFormalParameterToCaller()
                
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
            identifier = self.token.lexicalUnit
            self.__getNextToken()
            self.__assignStat(identifier)
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
            
    def __assignStat(self, identifier):
        if (self.token.lexicalUnit == ":="):
            self.__getNextToken()
            
            E_Place = self.__expression()
            self.intermediateCode.genQuad(":=", E_Place, "_", identifier)
        
        else:
            print("Expecting assign symbol ':=' at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'") 
            sys.exit() 

    def __ifStat(self):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            cond_true, cond_false = self.__condition()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
                
                self.intermediateCode.backpatch(cond_true, 
                                            self.intermediateCode.nextQuad())
                
                self.__statements()
                
                ifList = self.intermediateCode.makeList(
                    self.intermediateCode.nextQuad())
                self.intermediateCode.genQuad("jump", "_", "_", "_")
                self.intermediateCode.backpatch(cond_false, 
                                            self.intermediateCode.nextQuad())
                
                self.__elsepart()
                
                self.intermediateCode.backpatch(ifList, 
                                            self.intermediateCode.nextQuad())
                
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
            
            condQuad = self.intermediateCode.nextQuad()
            
            cond_true, cond_false = self.__condition()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
                
                self.intermediateCode.backpatch(cond_true, 
                                            self.intermediateCode.nextQuad())
                
                self.__statements()

                self.intermediateCode.genQuad("jump", "_", "_", condQuad)
                self.intermediateCode.backpatch(cond_false, 
                                            self.intermediateCode.nextQuad())
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
        exitList = self.intermediateCode.emptyList()
        
        while (self.token.lexicalUnit == "case"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "("):
                self.__getNextToken()
                
                cond_true, cond_false = self.__condition()
                
                if (self.token.lexicalUnit == ")"):
                    self.__getNextToken()
                    
                    self.intermediateCode.backpatch(cond_true, 
                                            self.intermediateCode.nextQuad())
                    
                    self.__statements()
                    
                    t = self.intermediateCode.makeList(
                        self.intermediateCode.nextQuad())
                    self.intermediateCode.genQuad("jump", "_", "_", "_")
                    exitList = self.intermediateCode.mergeList(exitList, t)
                    self.intermediateCode.backpatch(cond_false, 
                                            self.intermediateCode.nextQuad())
                    
                else:
                    print("Expecting closing bracket at ({},{})"
                          .format(self.token.position[0], 
                                  self.token.position[1])
                          + " instead received '" + self.token.lexicalUnit 
                          + "'") 
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
            
        self.intermediateCode.backpatch(exitList, 
                                        self.intermediateCode.nextQuad())

    def __forcaseStat(self):
        firstCondQuad = self.intermediateCode.nextQuad()
        
        while (self.token.lexicalUnit == "case"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "("):
                self.__getNextToken()
                
                cond_true, cond_false = self.__condition()
                
                if (self.token.lexicalUnit == ")"):
                    self.__getNextToken()
                    
                    self.intermediateCode.backpatch(cond_true, 
                                            self.intermediateCode.nextQuad())
                    
                    self.__statements()
                    
                    self.intermediateCode.genQuad("jump", "_", "_", 
                                                  firstCondQuad)
                    self.intermediateCode.backpatch(cond_false, 
                                            self.intermediateCode.nextQuad())
                    
                else:
                    print("Expecting closing bracket at ({},{})"
                          .format(self.token.position[0], 
                                  self.token.position[1])
                          + " instead received '" + self.token.lexicalUnit 
                          + "'") 
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
        flag = self.intermediateCode.newTemp()
        firstCondQuad = self.intermediateCode.nextQuad()
        self.intermediateCode.genQuad(":=", "0", "_", flag)
        
        # Symbols Table
        self.symbolsTable.addTemporaryVariable(flag)
        
        while (self.token.lexicalUnit == "case"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "("):
                self.__getNextToken()
                
                cond_true, cond_false = self.__condition()
                
                if (self.token.lexicalUnit == ")"):
                    self.__getNextToken()
                    
                    self.intermediateCode.backpatch(cond_true, 
                                            self.intermediateCode.nextQuad())
                    
                    self.__statements()
                    
                    self.intermediateCode.genQuad(":=", "1", "_", flag)
                    self.intermediateCode.backpatch(cond_false, 
                                            self.intermediateCode.nextQuad())
                    
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
            
        self.intermediateCode.genQuad("=", "1", flag, firstCondQuad)
                
    def __returnStat(self):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            E_Place = self.__expression()
            self.intermediateCode.genQuad("ret", "_", "_", E_Place)
            
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
            name = self.token.lexicalUnit
            
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
                
            self.intermediateCode.genQuad("call", name, "_", "_")
        else:
            print("Expecting variable name at ({},{})"
                  .format(self.token.position[0], self.token.position[1])
                  + " instead received '" + self.token.lexicalUnit + "'")
            sys.exit()
            
    def __printStat(self):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            E_Place = self.__expression()
            self.intermediateCode.genQuad("out", E_Place, "_", "_")
            
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
                
                id_Place = self.token.lexicalUnit
                self.intermediateCode.genQuad("in", id_Place, "_", "_")
                
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
        if (self.token.lexicalUnit in ["in", "inout"]): # new addition

            # Save parameters and return types to a list until all parameters
            # have been found. Then create groups of quads
            parameters = []
            returnTypes = []
            parameter, returnType = self.__actualparitem()
            parameters.append(parameter)
            returnTypes.append(returnType)
        
            while (self.token.lexicalUnit == ","):
                self.__getNextToken()
                
                parameter, returnType = self.__actualparitem()
                parameters.append(parameter)
                returnTypes.append(returnType)
                
            for i in range(len(parameters)):
                self.intermediateCode.genQuad("par", parameters[i], 
                                              returnTypes[i], "_")
                
    def __actualparitem(self):
        if (self.token.lexicalUnit == "in"):
            self.__getNextToken()

            E_Place = self.__expression()
            return E_Place, "CV"
        
        elif (self.token.lexicalUnit == "inout"):
            self.__getNextToken()
            if (self.token.family == "identifier"):
                
                identifier = self.token.lexicalUnit
                
                self.__getNextToken()
                
                return identifier, "REF"
            
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
            
    def __condition(self):
        B_true, B_false = self.__boolterm()
        
        while (self.token.lexicalUnit == "or"):
            self.intermediateCode.backpatch(B_false, 
                                            self.intermediateCode.nextQuad())
            
            self.__getNextToken()
            
            Q2_true, Q2_false = self.__boolterm()
            B_true = self.intermediateCode.mergeList(B_true, Q2_true)
            B_false = Q2_false
        
        return B_true, B_false
            
    def __boolterm(self):
        Q_true, Q_false = self.__boolfactor()
        
        while (self.token.lexicalUnit == "and"):
            self.intermediateCode.backpatch(Q_true, 
                                            self.intermediateCode.nextQuad())
            
            self.__getNextToken()

            R2_true, R2_false = self.__boolfactor()
            Q_false = self.intermediateCode.mergeList(Q_false, R2_false)
            Q_true = R2_true
        
        return Q_true, Q_false
            
    def __boolfactor(self):
        
        if (self.token.lexicalUnit == "not"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "["):
                self.__getNextToken()
                
                B_true, B_false = self.__condition()
                
                if (self.token.lexicalUnit == "]"):
                    self.__getNextToken()
                else:
                    print("Expecting closeing square bracket at ({},{})"
                          .format(self.token.position[0], 
                                  self.token.position[1])
                          + " instead received '" + self.token.lexicalUnit + "'") 
                    sys.exit() 
                    
                return B_false, B_true
                
            else:
                print("Expecting opening square bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 
        
        elif (self.token.lexicalUnit == "["):
            self.__getNextToken()

            B_true, B_false = self.__condition()

            if (self.token.lexicalUnit == "]"):
                self.__getNextToken()
            else:
                print("Expecting closeing square bracket at ({},{})"
                      .format(self.token.position[0], 
                              self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit() 

            return B_true, B_false
        
        else:

            E1_Place = self.__expression()
            
            if (self.token.lexicalUnit in self.REL_OP):
                rel_op = self.token.lexicalUnit
                
                self.__getNextToken()
            else:
                print("Expecting relational operator at ({},{})"
                      .format(self.token.position[0], self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'")
                sys.exit()
        
            E2_Place = self.__expression()
            R_true = self.intermediateCode.makeList(
                self.intermediateCode.nextQuad())
            self.intermediateCode.genQuad(rel_op, E1_Place, E2_Place, "_")
            R_false = self.intermediateCode.makeList(
                self.intermediateCode.nextQuad())
            self.intermediateCode.genQuad("jump", "_", "_", "_")
            return R_true, R_false
            

    def __expression(self):

        T1_Place = self.__optionalSign() + self.__term()
        
        while (self.token.lexicalUnit in self.ADD_OP):
            op = self.token.lexicalUnit
            
            self.__getNextToken()
                        
            T2_Place = self.__term()
            w = self.intermediateCode.newTemp()
            self.intermediateCode.genQuad(op, T1_Place, T2_Place, w)
            T1_Place = w
            
            # Symbols Table
            self.symbolsTable.addTemporaryVariable(w)
        
        return T1_Place
    
    def __term(self):
        
        F1_Place = self.__factor()
        
        while (self.token.lexicalUnit in self.MUL_OP):
            op = self.token.lexicalUnit
            
            self.__getNextToken()
            
            F2_Place = self.__factor()
            w = self.intermediateCode.newTemp()
            self.intermediateCode.genQuad(op, F1_Place, F2_Place, w)
            F1_Place = w
            
            # Symbols Table
            self.symbolsTable.addTemporaryVariable(w)
            
        return F1_Place

    def __factor(self):
        if (self.token.family == "number"):
            factor = self.token.lexicalUnit
            
            self.__getNextToken()
            
            return factor
        
        elif (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            factor = self.__expression()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
            else:
                print("Expecting closing bracket at ({},{})"
                      .format(self.token.position[0], 
                              self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit()
                
            return factor
        
        elif (self.token.family == "identifier"):
            identifier = self.token.lexicalUnit
            
            self.__getNextToken()
            
            return self.__idtail(identifier)

        
        else:
            print("Received invalid symbol {} at ({},{})"
                  .format(self.token.lexicalUnit, self.token.position[0], 
                          self.token.position[1])) 
            sys.exit()
            
    def __idtail(self, identifier):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            self.__actualparlist()

            w = self.intermediateCode.newTemp()
            self.intermediateCode.genQuad("par", w, "RET", "_")
            self.intermediateCode.genQuad("call", identifier, "_", "_")
            
            # Symbols Table
            self.symbolsTable.addTemporaryVariable(w)
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
            else:
                print("Expecting closeing bracket at ({},{})"
                      .format(self.token.position[0], 
                              self.token.position[1])
                      + " instead received '" + self.token.lexicalUnit + "'") 
                sys.exit()
        
            return w
        return identifier
                
    def __optionalSign(self):
        if (self.token.lexicalUnit in self.ADD_OP):
            sign = self.token.lexicalUnit
            self.__getNextToken()
            return sign
        return ""
    
class Quad:
    
    # Quad: label:[op, arg1, arg2, result]
    def __init__(self, label, operator, arg1, arg2, result):
        self.label = label
        self.operator = operator
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
        
    def toString(self):
        return (self.label + ": " + self.operator + ", " + self.arg1 + ", " 
                + self.arg2 + ", " + self.result)
    
    def toC(self):
        
        if self.operator == "begin_block":
            cCode = "L_" + self.label + ":"
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if self.operator == "end_block":
            cCode = "L_" + self.label + ": ;"
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if self.operator == "halt":
            cCode = "L_" + self.label + ": return(0);"
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == ":="):
            cCode = ("L_" + self.label + ": " + self.result + "=" + self.arg1 
                    + ";")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator in ["+", "-", "*", "/"]):
            cCode = ("L_" + self.label + ": " + self.result + "=" 
                    + self.arg1 + self.operator + self.arg2 + ";")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == "="):
            cCode = ("L_" + self.label + ": if (" + self.arg1 + "==" 
                    + self.arg2 + ") goto L_" + self.result + ";")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator in [">", "<", "<>", ">=", "<="]):
            cCode = ("L_" + self.label + ": if (" + self.arg1 + self.operator 
                    + self.arg2 + ") goto L_" + self.result + ";")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == "jump"):
            cCode = ("L_" + self.label + ": goto L_" + self.result + ";")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == "in"):
            cCode = ("L_" + self.label + ": scanf(\"%d\", &" + self.arg1 
                     + ");")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == "out"):
            cCode = ("L_" + self.label + ": printf(\"%d\\n\", " + self.arg1 
                     + ");")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == "ret"):
            cCode = ("L_" + self.label + ":return(" + self.arg1 + ");")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        
class IntermediateCode:
    
    def __init__(self):
        self.nextLabel = 100
        self.variableCounter = 0
        self.quads = []
        
    def genQuad(self, op, arg1, arg2, result):
        quad = Quad(str(self.nextLabel), op, arg1, arg2, result)
        self.quads.append(quad)
        self.nextLabel += 1
        return quad
        
    def nextQuad(self):
        return str(self.nextLabel)
        
    def newTemp(self):
        self.variableCounter += 1
        return "T_" + str(self.variableCounter)
        
    def emptyList(self):
        return []
        
    def makeList(self, label):
        return [label]
        
    def mergeList(self, list1, list2):
        return list1 + list2
        
    def backpatch(self, list, label):
        for l in list:
            self.quads[int(l)-100].result = label
        return
    
    def printOut(self):
        for quad in self.quads:
            print(quad.toString())
            
    def saveToFile(self):
        file = open("test.int", "w")
        for quad in self.quads:
            file.write(quad.toString() + "\n")
        file.close()
        
    def convertToC(self):
        cLines = ["#include <stdio.h>", "", "int main()", "{"]
        
        # Collect variables
        variables = self.__discoverVariables()
        if (len(variables) == 0):
            return
        
        variableLine = "int "
        for var in variables:
            variableLine += var + ","
        variableLine = variableLine[:-1] + ";"
        cLines.append(variableLine)
        
        # Construct remaining c lines
        for quad in self.quads:
            cLines.append(quad.toC())
        cLines.append("}")
        
        # Save to file
        file = open("test.c", "w")
        for line in cLines:
            file.write(line + "\n")
        file.close()

    def __discoverVariables(self):
        variables = set()
        
        for quad in self.quads:
            
            # if function/procedure is discovered -> exit
            if quad.operator == "par":
                return set()
            
            # skip some lines entirely
            if quad.operator in ["begin_block", "end_block", "halt", "jump"]:
                continue
            
            # everything which is not a number or "_" is a variable
            if (not quad.arg1.isdigit() and quad.arg1 != "_"):
                variables.add(quad.arg1)
            if (not quad.arg2.isdigit() and quad.arg2 != "_"):
                variables.add(quad.arg2)
            if (not quad.result.isdigit() and quad.result != "_"):
                variables.add(quad.result)

        return variables

class SymbolsTable:
    
    def __init__(self):
        self.scopes = []
        self.scopeStrings = []
        self.mainFrameLength = 0
    
    def getTopScopeSize(self):
        return self.scopes[-1].getSize()
    
    def addScope(self, scopeName):
        self.scopes.append(Scope(scopeName, len(self.scopes)))
        
    def removeLastScope(self):
        self.scopes.pop()
        
    def addProcedure(self, name):
        self.scopes[-1].addProcedure(name)
        
    def addFunction(self, name, datatype):
        self.scopes[-1].addFunction(name, datatype)        
    
    def addParameter(self, name, datatype, mode):
        self.scopes[-1].addParameter(name, datatype, mode)
        
    def addVariable(self, name):
        self.scopes[-1].addVariable(name)
        
    def addTemporaryVariable(self, name):
        self.scopes[-1].addTemporaryVariable(name)
        
    def appendFormalParameterToCaller(self):
        self.scopes[-2].appendFormalParameter(self.scopes[-1]
                                              .getLastFormalParameter())
        
    def fillInStartingQuad(self, quad):
        # We don't need to save the starting quad for main
        if (len(self.scopes) == 1):
            return
        
        self.scopes[-2].fillInStartingQuad(quad)
        
    def fillInFrameLength(self, frameLength):
        self.scopes[-1].fillInFrameLength(frameLength)
        
    def setMainFrameLength(self, frameLength):
        self.mainFrameLength = frameLength
    
    def saveScopeString(self):
        self.scopeStrings.append(self.scopes[-1].toString())
        
    def printScopeTrace(self):
        for scope in self.scopeStrings:
            print(scope)
            
    def saveScopeTraceToFile(self):
        file = open("test.symb", "w")
        file.write("# The below is the equivalent scope graph in text\n" 
                   + "# The number in parenthesis represents the scope level\n"
                   + "# The trace is recorded right before the scope is " 
                   + "closed. \n"
                   + "# The square brackets contain the functions/procedures "
                   + "formal parameters. \n")
        file.write("Scope trace: \n")
        for scope in self.scopeStrings:
            file.write(scope + "\n")
        file.close()
    
class Scope:
    
    def __init__(self, name, level):
        self.name = name
        self.nestingLevel = level
        self.entities = []
        self.offset = 12
        
    def getSize(self):
        return self.offset
    
    def addProcedure(self, name):
        self.entities.append(Procedure(name))
        
    def addFunction(self, name, datatype):
        self.entities.append(Function(name, datatype))
        
    def appendFormalParameter(self, formalParameter):
        self.entities[-1].addFormalParameter(formalParameter)
    
    def getLastFormalParameter(self):
        return self.entities[-1]
        
    def addParameter(self, name, datatype, mode):
        self.entities.append(Parameter(name, datatype, mode, self.offset))
        self.offset += 4
        
    def addVariable(self, name):
        self.entities.append(Variable(name, "int", self.offset))
        self.offset += 4
        
    def addTemporaryVariable(self, name):
        self.entities.append(TemporaryVariable(name, "int", self.offset))
        self.offset +=4
        
    def fillInStartingQuad(self, quad):
        self.entities[-1].setStartingQuad(quad)
    
    def fillInFrameLength(self, frameLength):
        self.entities[-1].setFrameLength(frameLength)
        
    def toString(self):
        return ("(" + str(self.nestingLevel) + ")" 
                + ''.join([entity.toString() for entity in self.entities]))
    

class Entity(ABC):
    def __init__(self, name):
        self.name = name

class Variable(Entity):
    def __init__(self, name, datatype, offset):
        super().__init__(name)
        self.datatype = datatype
        self.offset = offset
    
    def toString(self):
        return("<--(" + self.name + "/" + self.datatype + "/" 
              + str(self.offset) + ")")
    
class TemporaryVariable(Variable):
    def __init__(self, name, datatype, offset):
        super().__init__(name, datatype, offset)
        
    def toString(self):
        return("<--(" + self.name + "/" + self.datatype + "/" 
              + str(self.offset) + ")")
      
# e.g procedure P1(in x, inout y) {...}
class FormalParameter(Entity):
    def __init__(self, name, datatype, mode):
        super().__init__(name)
        self.datatype = datatype
        self.mode = mode
    
    def toString(self):
        return("<--(" + self.name + "/" + self.datatype + "/" + self.mode 
               + ")")
    
    def toString2(self):
        return("(" + self.name + "/" + self.datatype + "/" + self.mode 
               + ")")
     
# e.g. call P1(in a, inout b);
class Parameter(FormalParameter):    
    # name is not necessary but for consistency
    def __init__(self, name, datatype, mode, offset):
        super().__init__(name, datatype, mode)
        self.offset = offset
    
    def toString(self):
        return("<--(" + self.name + "/" + self.datatype + "/" 
              + self.mode + "/" + str(self.offset) + ")")
    
    def toString2(self):
        return("(" + self.name + "/" + self.datatype + "/" 
              + self.mode + "/" + str(self.offset) + ")")
    
class Procedure(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.startingQuad = ""
        self.frameLength = ""
        self.formalParameters = []

    def setStartingQuad(self, quad):
        self.startingQuad = quad
        
    def setFrameLength(self, length):
        self.frameLength = length
        
    def addFormalParameter(self, param):
        self.formalParameters.append(param)
        
    def toString(self):
        return("<--(" + self.name + "/" + self.startingQuad + "/" 
              + str(self.frameLength) + "/[" 
              + ''.join([param.toString2() for param in self.formalParameters]) 
              + "])")
             
class Function(Procedure):
    def __init__(self, name, datatype):
        super().__init__(name)
        self.datatype = datatype
        
    def toString(self):
        return("<--(" + self.name + "/" + self.datatype + "/" 
              + self.startingQuad + "/" + str(self.frameLength) + "/[" 
              + ''.join([param.toString2() for param in self.formalParameters])
              + "])")
        
# Cimple does not support symbolic constants.
class SumbolicConstant(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.value = ""
        
    def toString(self):
        return("<-- (" + self.name + "/ " + self.value + ")")
    
if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Wrong arguments. Must give just the filename")
        sys.exit()

    filename = sys.argv[1]
    
    syntaxAnalyser = SyntaxAnalyser(filename)
    syntaxAnalyser.run()