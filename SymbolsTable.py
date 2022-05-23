"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

import sys
from abc import ABC

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
        
    def fillInStartingQuad(self, quadLabel):
        # We don't need to save the starting quad for main
        if (len(self.scopes) == 1):
            return
        
        self.scopes[-2].fillInStartingQuad(quadLabel)
        
    def fillInFrameLength(self, frameLength):
        # self.scopes[-1].fillInFrameLength(frameLength)
        self.scopes[-2].fillInFrameLength(frameLength)
        
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
    
    def isVariableGlobal(self, v):
        return self.scopes[0].isVariableInScope(v)
    
    def isVariableInCurrentScope(self, v):
        return self.scopes[-1].isVariableInScope(v)
    
    def isVariableInHigherScopeLowerThanMain(self, v):
        for scope in reversed(self.scopes[1:-1]):
            if scope.isVariableInScope(v):
                return True
        return False

    def getOffsetFromMain(self, v):
        return self.scopes[0].getOffset(v)
    
    def getFrameLengthFromMain(self, v):
        return self.scopes[0].getFrameLength(v)
    
    def getStartingQuadFromMain(self, v):
        return self.scopes[0].getStartingQuad(v)
    
    def getOffsetFromCurrentScope(self, v):
        return self.scopes[-1].getOffset(v)
    
    def getPassingModeFromCurrentScope(self, v):
        return self.scopes[-1].getPassingMode(v)
    
    def getFrameLengthFromCurrentScope(self, v):
        return self.scopes[-1].getFrameLength(v)
    
    def getStartingQuadFromCurrentScope(self, v):
        return self.scopes[-1].getStartingQuad(v)
          
    def getNumberOfLevelsAbove(self, v):
        levels = 0
        # We want to look only to higher scopes i.e. scopes[:-1]
        for scope in reversed(self.scopes[:-1]):
            levels += 1
            if scope.isVariableInScope(v):
                return levels
        
        print("Could not find variable {} in symbols table!)".format(v))
        sys.exit()
    
    def getOffsetFromHigherScope(self, v):
        return self.__getHigherScope(v).getOffset(v)
    
    def getPassingModeFromHigherScope(self, v):
        return self.__getHigherScope(v).getPassingMode(v)
    
    def getFrameLengthFromHigherScope(self, v):
        return self.__getHigherScope(v).getFrameLength(v)
    
    def getStartingQuadFromHigherScope(self, v):
        return self.__getHigherScope(v).getStartingQuad(v)
    
    def isMainScopeCurrent(self):
        return len(self.scopes) == 1
    
    def __getHigherScope(self, v):
        # We want to look only to higher scopes i.e. scopes[:-1]
        for scope in reversed(self.scopes[:-1]):
            if scope.isVariableInScope(v):
                return scope
            
        print("Could not find variable {} in symbols table!)".format(v))
        sys.exit() 
    
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
        
    def fillInStartingQuad(self, quadLabel):
        self.entities[-1].setStartingQuad(quadLabel)
    
    def fillInFrameLength(self, frameLength):
        self.entities[-1].setFrameLength(frameLength)
        
    def toString(self):
        return ("(" + str(self.nestingLevel) + ")" 
                + ''.join([entity.toString() for entity in self.entities]))
    
    def isVariableInScope(self, v):
        for entity in self.entities:
            if entity.getName() == v:
                return True
        return False
    
    def getOffset(self, v):
        return self.__getEntityInScope(v).getOffset()
         
    def getPassingMode(self, v):
        return self.__getEntityInScope(v).getPassingMode()
        
    def getFrameLength(self, v):
        return self.__getEntityInScope(v).getFrameLength()
            
    def getStartingQuad(self, v):
        return self.__getEntityInScope(v).getStartingQuad()
        
    def __getEntityInScope(self, v):
        for entity in self.entities:
            if entity.getName() == v:
                return entity
        
        print("Variable {} not in current scope ({})!)"
              .format(v, self.nestingLevel))
        sys.exit()
            

class Entity(ABC):
    def __init__(self, name):
        self.name = name
        
    def getName(self):
        return self.name;
    
    def getOffset(self):
        return -1
    
    def getPassingMode(self):
        return ""
    
    def getFrameLength(self):
        return -1
    
    def getStartingQuad(self):
        return ""

class Variable(Entity):
    def __init__(self, name, datatype, offset):
        super().__init__(name)
        self.datatype = datatype
        self.offset = offset
    
    def toString(self):
        return("<--(" + self.name + "/" + self.datatype + "/" 
              + str(self.offset) + ")")
    
    def getOffset(self):
        return self.offset
    
class TemporaryVariable(Variable):
    def __init__(self, name, datatype, offset):
        super().__init__(name, datatype, offset)
        
    def toString(self):
        return("<--(" + self.name + "/" + self.datatype + "/" 
              + str(self.offset) + ")")
    
    def getOffset(self):
        return self.offset
      
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
    
    def getPassingMode(self):
        return self.mode
     
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
    
    def getOffset(self):
        return self.offset
    
class Procedure(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.startingQuad = ""
        self.frameLength = ""
        self.formalParameters = []

    def setStartingQuad(self, quadLabel):
        self.startingQuad = quadLabel
        
    def setFrameLength(self, length):
        self.frameLength = length
        
    def addFormalParameter(self, param):
        self.formalParameters.append(param)
        
    def toString(self):
        return("<--(" + self.name + "/" + self.startingQuad + "/" 
              + str(self.frameLength) + "/[" 
              + ''.join([param.toString2() for param in self.formalParameters]) 
              + "])")
    
    def getFrameLength(self):
        return self.frameLength
    
    def getStartingQuad(self):
        return self.startingQuad
             
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
    
    
# test Intermediate code
if __name__ == "__main__":
    
    variable = Variable("x", "int", 12)
    print("Variable: " + variable.toString())
    print("Name: " + variable.getName())
    print("offset: " + str(variable.getOffset()))
    print("Passing mode: " + variable.getPassingMode())
    
    tempVariable = TemporaryVariable("T_1", "int", 16)
    print("Temporary Variable: " + tempVariable.toString())
    print("Name: " + tempVariable.getName())
    print("offset: " + str(tempVariable.getOffset()))
    print("Passing mode: " + tempVariable.getPassingMode())
    
    formalParameter1 = FormalParameter("a", "int", "cv")
    print("Formal Parameter: " + formalParameter1.toString())
    print("Name: " + formalParameter1.getName())
    print("Passing mode: " + formalParameter1.getPassingMode())
    
    formalParameter2 = FormalParameter("b", "int", "ref")
    print("Formal Parameter: " + formalParameter2.toString())
    print("Name: " + formalParameter2.getName())
    print("Passing mode: " + formalParameter2.getPassingMode())
    
    parameter = Parameter("c", "int", "cv", 20)
    print("Parameter: " + parameter.toString())
    print("Name: " + parameter.getName())
    print("Passing mode: " + parameter.getPassingMode())
    
    procedure = Procedure("P1")
    procedure.setFrameLength(24)
    procedure.setStartingQuad("100")
    procedure.addFormalParameter(formalParameter1)
    procedure.addFormalParameter(formalParameter2)
    print("Procedure: " + procedure.toString())
    print("Name: " + procedure.getName())
    
    function = Function("F1", "int")
    function.setFrameLength(48)
    function.setStartingQuad("200")
    function.addFormalParameter(formalParameter1)
    function.addFormalParameter(formalParameter2)
    print("Function: " + function.toString())
    print("Name: " + function.getName())
    