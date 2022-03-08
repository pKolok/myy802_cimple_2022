"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

import sys
from LexicalAnalyser import LexicalAnalyser

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
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit() 
            
        else:
            print("Expecting opening curly bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])) 
            sys.exit() 
            
            
    def __declarations(self):
        while (self.token.lexicalUnit == "declare"):
            self.__getNextToken()
            
            self.__varlist()
            
            if (self.token.lexicalUnit == ";"):
                self.__getNextToken()
            else:
                print("Expecting delimiter ';' at ({},{})"
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit() 
        
        # can have no declarations so no else here needed.
                
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
                                  self.token.position[1])) 
                    sys.exit() 
            else:
                print("Expecting opening bracket at ({},{})"
                      .format(self.token.position[0], 
                              self.token.position[1])) 
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
        if (self.token.lexicalUnit in ["in", "out"]):
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
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit() 
        else:
            self.__statement()
            
            if (self.token.lexicalUnit == ";"):
                self.__getNextToken()
            else:
                print("Expecting delimiter ';' at ({},{})"
                      .format(self.token.position[0], self.token.position[1])) 
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
                  .format(self.token.position[0], self.token.position[1])) 
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
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit() 
        else:
            print("Expecting opening bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])) 
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
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit() 
        else:
            print("Expecting opening bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])) 
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
                          .format(self.token.position[0], self.token.position[1])) 
                    sys.exit() 
            else:
                print("Expecting opening bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit()
            
        if (self.token.lexicalUnit == "default"):
            self.__getNextToken()
            
            self.__statements()

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
                          .format(self.token.position[0], self.token.position[1])) 
                    sys.exit() 
            else:
                print("Expecting opening bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit()
            
        if (self.token.lexicalUnit == "default"):
            self.__getNextToken()
            
            self.__statements()
            
    def __incase(self):
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
                          .format(self.token.position[0], self.token.position[1])) 
                    sys.exit() 
            else:
                print("Expecting opening bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit()
                
    def __returnStat(self):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            self.__expression()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
                
            else:
                print("Expecting closing bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit() 
        else:
            print("Expecting opening bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])) 
            sys.exit()
            
    def __callStat(self):
        if (self.token.family == "intentifier"):
            self.__getNextToken()
            
            if (self.token.lexicalUnit == "("):
                self.__getNextToken()
                
                self.__actualparlist()
                
                if (self.token.lexicalUnit == ")"):
                    self.__getNextToken()
                    
                else:
                    print("Expecting closing bracket at ({},{})"
                          .format(self.token.position[0], self.token.position[1])) 
                    sys.exit() 
            else:
                print("Expecting opening bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])) 
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
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit() 
        else:
            print("Expecting opening bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])) 
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
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit() 
        else:
            print("Expecting opening bracket at ({},{})"
                  .format(self.token.position[0], self.token.position[1])) 
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
                                  self.token.position[1])) 
                    sys.exit() 
                
            else:
                print("Expecting opening square bracket at ({},{})"
                      .format(self.token.position[0], self.token.position[1])) 
                sys.exit() 
        
        elif (self.token.lexicalUnit == "["):
            self.__getNextToken()
            
            self.__condition()

            if (self.token.lexicalUnit == "]"):
                self.__getNextToken()
            else:
                print("Expecting closeing square bracket at ({},{})"
                      .format(self.token.position[0], 
                              self.token.position[1])) 
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
                              self.token.position[1])) 
                sys.exit()
        
        elif (self.token.family == "identifier"):
            self.__getNextToken()
            
            self.__idtail()
            
    def __idtail(self):
        if (self.token.lexicalUnit == "("):
            self.__getNextToken()
            
            self.__actualparlist()
            
            if (self.token.lexicalUnit == ")"):
                self.__getNextToken()
            else:
                print("Expecting closeing bracket at ({},{})"
                      .format(self.token.position[0], 
                              self.token.position[1])) 
                sys.exit()
                
    def __optionalSign(self):
        if (self.token.lexicalUnit in self.ADD_OP):
            self.__getNextToken()


    

if __name__ == "__main__":
    
    syntaxAnalyser = SyntaxAnalyser("countDigits.c")
    syntaxAnalyser.run()
    
    syntaxAnalyser = SyntaxAnalyser("factorial.c")
    syntaxAnalyser.run()
    
    syntaxAnalyser = SyntaxAnalyser("fibonacci.c")
    syntaxAnalyser.run()
    
    syntaxAnalyser = SyntaxAnalyser("primes.c")
    syntaxAnalyser.run()
    
    syntaxAnalyser = SyntaxAnalyser("summation.c")
    syntaxAnalyser.run()
        