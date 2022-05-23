"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

import sys

class FinalCode:
    
    def __init__(self, intermediateCode, symbolsTable):
        self.finalCode = []
        self.intermediateCode = intermediateCode
        self.symbolsTable = symbolsTable
        self.quadListIndex = 0
        self.arithOp = {"+" : "add", "-" : "sub", "*" : "mul", "/" : "div"}
        self.logicOp = {"=" : "beq", "<=" : "ble", ">=" : "bge", ">" : "bgt",
                        "<" : "blt", "<>" : "bne"}
        self.executedOnce = False

    def printToScreen(self):
        for codeLine in self.finalCode:
            print(codeLine)
    
    def writeToFile(self):
        file = open("test.asm", "w")
        for line in self.finalCode:
            file.write(line + "\n")
        file.close()

    def generateFinalCode(self, framelength):
        
        # First get the list of quads generated already
        quads = self.intermediateCode.getListOfQuads()
        
        # Very first command of every program - only executed once
        if (not self.executedOnce): 
            self.__produce("L000:")
            self.__produce("\t\tj main")
            self.executedOnce = True
        
        parFound = False
        numberOfParameters = 0
        
        # Then loop through quads not visited before
        # for index in range(self.quadListIndex, len(quads)):
        while (self.quadListIndex < len(quads)):            
            quad = quads[self.quadListIndex]
            
            # Assignment
            if (quad.getOperator() == ":="):
                self.__produceLabel(quad)
                self.__loadvr(quad.getArg1(), 't1')
                self.__storerv('t1', quad.getResult())
            
            # Arithmetic operation
            elif (quad.getOperator() in ["+", "-", "*", "/"]):
                op = quad.getOperator()
                self.__produceLabel(quad)
                self.__loadvr(quad.getArg1(), 't1')
                self.__loadvr(quad.getArg2(), 't2')              
                self.__produce("\t\t" + self.arithOp[op] + ' t1, t1, t2')
                self.__storerv('t1', quad.getResult())
            
            # Simple jump i.e. jump
            elif (quad.getOperator() == "jump"):
                self.__produceLabel(quad)
                self.__produce("\t\tj " + quad.getResult())
            
            # Logical jump
            elif (quad.getOperator() in ["==", "<=", ">=", ">", "<", "<>"]):
                op = quad.getOperator()
                self.__produceLabel(quad)
                self.__loadvr(quad.getArg1(), "t1")
                self.__loadvr(quad.getArg2(), "t2")
                self.__produce("\t\t" + self.logicOp[op] + " t1, t2, " 
                               + quad.getResult())
            
            # Begin of a block
            elif (quad.getOperator() == "begin_block"):
                
                # The new block is main
                if (self.symbolsTable.isMainScopeCurrent()):
                    self.__produce("main:")
                    self.__produceLabel(quad)
                    self.__produce("\t\taddi sp, sp, " + str(framelength))
                    self.__produce("\t\tmv gp, sp")
                    
                # The new block is a function/procedure
                else:
                    self.__produceLabel(quad)
                    self.__produce("\t\tsw ra, (sp)")
            
            # End of a block
            elif (quad.getOperator() == "end_block"):
                
                if (self.symbolsTable.isMainScopeCurrent()):
                    self.__produceLabel(quad)
                else:
                    self.__produceLabel(quad)
                    self.__produce("\t\tlw ra, (sp)")
                    self.__produce("\t\tjr ra")
            
            # End of program
            elif (quad.getOperator() == "halt"):
                self.__produceLabel(quad)
                self.__produce("\t\tli a0, 0")
                self.__produce("\t\tli a7, 93")
                self.__produce("\t\tecall")
            
            # Passing parameters in function/procedure
            elif (quad.getOperator() == "par"):
                
                self.__produceLabel(quad)
                
                # setup fp once (first time a par is found)
                if (not parFound):
                    
                    # Look forward at "call" quad to retrieve 
                    # function's/procedure's frame length
                    for tmpQuad in quads[self.quadListIndex + 1:]:
                        if (tmpQuad.getOperator() == "call"):
                            v = tmpQuad.getArg1()
                            if (self.symbolsTable.isVariableInCurrentScope(v)):
                                # offset, passMode, calleFrameLength = (
                                #     self.symbolsTable.lookAtCurrentScopeFor(v))
                                calleeFrameLength = (self.symbolsTable
                                        .getFrameLengthFromCurrentScope(v))
                            elif (self.symbolsTable
                                  .isVariableInHigherScopeLowerThanMain(v)):
                                # levels, offset, passMode, calleFrameLength = (
                                #     self.symbolsTable.lookAtHigherScopeFor(v))
                                calleeFrameLength = (self.symbolsTable
                                            .getFrameLengthFromHigherScope(v))
                            elif (self.symbolsTable.isVariableGlobal(v)):
                                # offset, calleFrameLength  = (
                                #     self.symbolsTable.lookAtMainFor(v))
                                calleeFrameLength = (self.symbolsTable
                                                    .getFrameLengthFromMain(v))
                            else:
                                print("Could not find variable {} in symbols" 
                                      " table!)".format(v))
                                sys.exit()    
        
                            self.__produce("\t\taddi fp, sp, " 
                                           + str(calleeFrameLength))
                            
                            # Flag that "par" quad was found
                            parFound = True;
                            
                            # Don't look into any more forward quads
                            break
                
                # Pass by value
                if (quad.getArg2() == "CV"):
                    self.__loadvr(quad.getArg1(), "t0")
                    d = 12 + 4 * numberOfParameters
                    self.__produce("\t\tsw t0, -" + str(d) + "(fp)")
                    numberOfParameters += 1
                
                # Pass by reference
                elif (quad.getArg2() == "REF"):
                    v = quad.getArg1()
                    d = 12 + 4* numberOfParameters
                    
                    # Variable v is in same scope as function/procedure to be
                    # called i.e. current scope
                    if (self.symbolsTable.isVariableInCurrentScope(v)):
                        # offset, passMode, frameLength = (self.symbolsTable
                        # .lookAtCurrentScopeFor(v))
                        offset = self.symbolsTable.getOffsetFromCurrentScope(v)
                        passMode = (self.symbolsTable
                                    .getPassingModeFromCurrentScope(v))
                        
                        # Variable v is parameter passed in by reference
                        if (passMode == "ref"):
                            self.__produce("\t\tlw t0, -" + str(offset) 
                                           + "(sp)")
                        
                        # Variable v is local variable or temp variable or
                        # parameter passed in by value
                        else:
                            self.__produce("\t\taddi t0, sp, -" + str(offset))
                        
                        # In both cases
                        self.__produce("\t\tsw t0, -" + str(d) + "(fp)")
                    
                    # Variable v is in a higher scope then function/procedure 
                    # to be called. If not -> error message
                    elif (self.symbolsTable
                          .isVariableInHigherScopeLowerThanMain(v)):
                        # levels, offset, passMode, frameLength = (
                        #     self.symbolsTable.lookAtHigherScopeFor(v))
                        passMode = (self.symbolsTable
                                    .getPassingModeFromHigherScope(v))
                        
                        # Variable v is parameter passed in by reference
                        if (passMode == "ref"):
                            self.__gnlvcode(v)
                            self.__produce("\t\tlw t0, (t0)")
                            
                        # Variable v is parameter passed in by value
                        else:
                            self.__gnlvcode(v)
                            
                        # In both cases
                        self.__produce("\t\tsw t0, -" + str(d) + "(fp)")
                    
                    # Variable v is global
                    elif (self.symbolsTable.isVariableGlobal(v)):
                        # offset, frameLength = (
                        #     self.symbolsTable.lookAtMainFor(v))
                        offset = self.symbolsTable.getOffsetFromMain(v)
                        
                        self.__produce("\t\taddi t0, gp, -" + str(offset))
                        self.__produce("\t\tsw t0, -" + str(d) + "(fp)")
                        
                    else:
                        print("Could not find variable {} in symbols table!)"
                              .format(v))
                        sys.exit()                        
                    
                    numberOfParameters += 1
    
                # Return parameter
                elif (quad.getArg2() == "RET"):
                    v = quad.getArg1()
                    # offset, passMode, frameLength = (self.symbolsTable
                    #                     .lookAtCurrentScopeFor(quad.getArg1()))
                    offset = self.symbolsTable.getOffsetFromCurrentScope(v)
                    
                    self.__produce("\t\taddi t0, sp, -" + str(offset))
                    self.__produce("\t\tsw t0, -8(fp)")
                    
                
            elif (quad.getOperator() == "call"):
                
                self.__produceLabel(quad)
                
                numberOfParameters = 0
                
                callee = quad.getArg1()

                # Look for framelength of function/procedure about to be
                # called
                if (self.symbolsTable.isVariableInCurrentScope(callee)):
                    # offset, passMode, calleFrameLength = (
                    #     self.symbolsTable.lookAtCurrentScopeFor(v))
                    calleeFrameLength = (self.symbolsTable
                                    .getFrameLengthFromCurrentScope(callee))
                    calleeStartingQuad = (self.symbolsTable
                                   .getStartingQuadFromCurrentScope(callee))
                    
                elif (self.symbolsTable
                      .isVariableInHigherScopeLowerThanMain()):
                    # levels, offset, passMode, calleFrameLength = (
                    #     self.symbolsTable.lookAtHigherScopeFor(v))
                    calleeFrameLength = (self.symbolsTable
                                        .getFrameLengthFromHigherScope(callee))
                    calleeStartingQuad = (self.symbolsTable
                                      .getStartingQuadFromHigherScope(callee))
                    
                elif (self.symbolsTable.isVariableGlobal(v)):
                    # offset, calleFrameLength  = (
                    #     self.symbolsTable.lookAtMainFor(v))
                    calleeFrameLength = (self.symbolsTable
                                        .getFrameLengthFromMain(callee))
                    calleeStartingQuad = (self.symbolsTable
                                          .getStartingQuadFromMain(callee))
                    
                else:
                    print("Could not find variable {} in symbols" 
                          " table!)".format(v))
                    sys.exit()    

                # set up fp once (if no "par" was earlier found)
                if (not parFound):

                    self.__produce("\t\taddi fp, sp, " 
                                   + str(calleeFrameLength))
                    parFound = True;         
                
                # Caller and callee have diff depth i.e. caller is parent of
                # callee. 
                if (self.symbolsTable.isVariableInCurrentScope(callee)):
                    self.__produce("\t\tsw sp, -4(fp)")
                
                # Caller and callee have same depth i.e. same parent
                else:
                    self.__produce("\t\tlw t0, -4(sp)")
                    self.__produce("\t\tsw t0, -4(fp)")
            
                # Transfer sp to callee
                self.__produce("\t\taddi sp, sp, " + str(calleeFrameLength))
                
                # Call function/procedure
                self.__produce("\t\tjal L" + str(int(calleeStartingQuad) - 1))
                
                # Return sp to caller
                self.__produce("\t\taddi sp, sp, -" + str(calleeFrameLength))              
                
            elif (quad.getOperator() == "ret"):
                self.__produceLabel(quad)

                self.__loadvr(quad.getResult(), "t1")
                self.__produce("\t\tlw t0, -8(sp)")
                self.__produce("\t\tsw t1, (t0)")
            
            elif (quad.getOperator() == "in"):
                self.__produceLabel(quad)
                
                self.__produce("\t\tli a7, 5")
                self.__produce("\t\tecall")
                self.__storerv('a0', quad.getArg1())
            
            elif (quad.getOperator() == "out"):
                self.__produceLabel(quad)
                
                self.__loadvr(quad.getArg1(), 'a0')
                self.__produce("\t\tli a7, 1")
                self.__produce("\t\tecall")
            
            self.quadListIndex += 1

    def __produce(self, codeLine):
        # TODO he is asking to output directly to file so i may need to change 
        # this implementation
        self.finalCode.append(codeLine)
    
    def __gnlvcode(self, v):
        """
        Produces final code for accessing variables or address saved in an
        activity register other than the one of the function under translation.
         - If the VALUE of a variable is requested, then the variable's address 
        will be stored in register t0.
         - If the ADDRESS of a variable is requested, then the address, which 
        contains the address of the requested variable, will be stored in t0.
        v: Variable whose value or address we wish to access.
        """
        # 1st: go to parent
        self.__produce('\t\tlw t0, -4(sp)')
        
        # 2nd: if variable is higher than parent climb up 'levelsUp' levels
        # levelsUp, offset, passMode, frameLength = (
        #     self.symbolsTable.lookAtHigherScopeFor(v))
        if (self.symbolsTable.isVariableInHigherScopeLowerThanMain(v)):
            levelsUp = self.symbolsTable.getNumberOfLevelsAbove(v)
            offset = self.symbolsTable.getOffsetFromHigherScope(v)
        
            for level in range(levelsUp - 1):
                self.__produce('\t\tlw t0, -4(t0)')
                
            # 3rd: account for offset
            self.__produce('\t\taddi t0, t0, -' + str(offset))

        else:
            print("Could not find variable {} in symbols table!)".format(v))
            sys.exit()            
        
    def __loadvr(self, v, reg):
        # v: source variable
        # reg: target register
        
        # If v is integer constant
        if (v.isnumeric()):
            self.__produce("\t\tli " + reg + ", " + v)
        
        # If variable is in current scope
        elif (self.symbolsTable.isVariableInCurrentScope(v)):
            # offset, passMode, frameLength = (
            #     self.symbolsTable.lookAtCurrentScopeFor(v))
            offset = self.symbolsTable.getOffsetFromCurrentScope(v)
            passMode = self.symbolsTable.getPassingModeFromCurrentScope(v)
            
            if (passMode != "ref"):
                # if local variable or passed by value or temporary variable
                self.__produce("\t\tlw " + reg + ", -" + str(offset) + "(sp)")
            else:
                # if passed by reference
                self.__produce("\t\tlw t0, -" + str(offset) + "(sp)")
                self.__produce("\t\tlw " + reg + ", (t0)")
            
        # If variable is not in current scope        
        elif (self.symbolsTable.isVariableInHigherScopeLowerThanMain(v)):
            # levelsUp, offset, passMode, frameLength = (
            #     self.symbolsTable.lookAtHigherScopeFor(v))
            passMode = self.symbolsTable.getPassingModeFromHigherScope(v)
            
            if (passMode != "ref"):
                # if local variable or passed by value or temporary variable:
                self.__gnlvcode(v)
                self.__produce("\t\tlw " + reg + ", (t0)")
            else:
                # if passed by reference
                self.__gnlvcode(v)
                self.__produce("\t\tlw t0, (t0)")
                self.__produce("\t\tlw " + reg + ", (t0)")
                
        # if variable is global variable i.e. defined in main
        elif(self.symbolsTable.isVariableGlobal(v)):
            # offset, frameLength = self.symbolsTable.lookAtMainFor(v)
            offset = self.symbolsTable.getOffsetFromMain(v)
            
            self.__produce("\t\tlw " + reg + ", -" + str(offset) + "(gp)")
            
        else:
            print("Could not find variable {} in symbols table!)".format(v))
            sys.exit()
            
    
    def __storerv(self, reg, v):
        # reg: source register
        # v: target variable
        
        # # If v is integer constant
        # if (v.isnumeric()):
        #     self.__loadvr(v, reg)
        #     self.__produce("sw " + reg + ", (t0)")
        
        # If variable is in current scope
        if (self.symbolsTable.isVariableInCurrentScope(v)):
            # offset, passMode, frameLength = (
            #     self.symbolsTable.lookAtCurrentScopeFor(v))
            offset = self.symbolsTable.getOffsetFromCurrentScope(v)
            passMode = self.symbolsTable.getPassingModeFromCurrentScope(v)
            
            if (passMode != "ref"):
                # if local variable or passed by value or temporary variable
                self.__produce("\t\tsw " + reg + ", -" + str(offset) + "(sp)")
            else:
                # if passed by reference
                self.__produce("\t\tlw t0, -" + str(offset) + "(sp)")
                self.__produce("\t\tsw " + reg + ", (t0)")
            
        # If variable is not in current scope
        elif (self.symbolsTable.isVariableInHigherScopeLowerThanMain(v)):            
            # levelsUp, offset, passMode, frameLength = (
            #     self.symbolsTable.lookAtHigherScopeFor(v))
            passMode = self.symbolsTable.getPassingModeFromHigherScope(v)
            
            if (passMode != "ref"):
                # if local variable or passed by value or temporary variable
                self.__gnlvcode(v)
                self.__produce("\t\tsw " + reg + ", (t0)")
            else:
                # if passed by reference
                self.__gnlvcode(v)
                self.__produce("\t\tlw t0, (t0)")
                self.__produce("\t\tsw " + reg + ", (t0)")
            
        # if variable is global variable i.e. defined in main
        elif (self.symbolsTable.isVariableGlobal(v)):
            # offset, frameLength = self.symbolsTable.lookAtMainFor(v)
            offset = self.symbolsTable.getOffsetFromMain(v)
            
            self.__produce("\t\tsw " + reg + ", -" + str(offset) + "(gp)")

        else:
            print("Could not find variable {} in symbols table!)".format(v))
            sys.exit()            
    

    def __produceLabel(self, quad):
        self.__produce("L" + quad.getLabel() + ":")
        
