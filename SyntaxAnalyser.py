"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

import sys
from LexicalAnalyser import LexicalAnalyser
from IntermediateCode import IntermediateCode
from SymbolsTable import SymbolsTable

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
        print("Intermediate Code:")
        self.intermediateCode.print()
        self.intermediateCode.saveToFile()
        self.intermediateCode.convertToC()
    
    def __getNextToken(self):
        self.token = self.lexicalAnalyser.getNextLexicalUnit()

    def __program(self):
        if (self.token.lexicalUnit == "program"):
            
            self.__getNextToken()
            
            if (self.token.family == "identifier"):
                name = self.token.lexicalUnit
            
                self.__getNextToken()

                self.__programBlock(name)
                
                self.intermediateCode.genQuad("halt", "_", "_", "_")
                self.intermediateCode.genQuad("end_block", name, "_", "_")

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
        
    def __programBlock(self, name):
        if (self.token.lexicalUnit == "{"):
            self.__getNextToken()
            
            self.__declarations()
            self.__subprograms()
            
            self.intermediateCode.genQuad("begin_block", name, "_", "_")
            
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
            
    def __subprograms(self):
        while (self.token.lexicalUnit in ["function", "procedure"]):
            self.__getNextToken()
            
            name = self.token.lexicalUnit
            
            self.__subprogram(name)
            
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
        if (self.token.lexicalUnit in ["in", "inout"]):
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
            self.intermediateCode.genQuad("ret", E_Place, "_", "_")
            
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
            # have been found. Then create groups of four
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
        self.__optionalSign()

        T1_Place = self.__term()
        
        while (self.token.lexicalUnit in self.ADD_OP):
            op = self.token.lexicalUnit
            
            self.__getNextToken()
                        
            T2_Place = self.__term()
            w = self.intermediateCode.newTemp()
            self.intermediateCode.genQuad(op, T1_Place, T2_Place, w)
            T1_Place = w
        
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
            self.__getNextToken()
    

if __name__ == "__main__":
    
    ### Test Syntax Analyser ###
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/countDigits.c")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/factorial.c")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/fibonacci.c")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/primes.c")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/summation.c")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/test.c")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/_armstrong.ci")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/_factorialnew.ci")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/_HappyDay.ci")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/_max3.ci")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/_pap.ci")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/_power.ci")
    # syntaxAnalyser.run()
    # syntaxAnalyser = SyntaxAnalyser("SyntaxAnalyserTests/_test_parser.ci")
    # syntaxAnalyser.run()
    
    ### Test Intermediate Code ###
    # syntaxAnalyser = SyntaxAnalyser("IntermediateCodeTests/ifWhile.c")
    # syntaxAnalyser.run()
    
    ### Test Symbols Table ###
    syntaxAnalyser = SyntaxAnalyser("SymbolsTableTests/symbol.c")
    syntaxAnalyser.run()