"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

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
    
    
# test Intermediate code
if __name__ == "__main__":
    
    variable = Variable("x", "int", 12)
    print("Variable: " + variable.toString())
    
    tempVariable = TemporaryVariable("T_1", "int", 16)
    print("Temporary Variable: " + tempVariable.toString())
    
    formalParameter1 = FormalParameter("a", "int", "cv")
    print("Formal Parameter: " + formalParameter1.toString())
    
    formalParameter2 = FormalParameter("b", "int", "ref")
    print("Formal Parameter: " + formalParameter2.toString())
    
    parameter = Parameter("c", "int", "cv", 20)
    print("Parameter: " + parameter.toString())
    
    procedure = Procedure("P1")
    procedure.setFrameLength(24)
    procedure.setStartingQuad("100")
    procedure.addFormalParameter(formalParameter1)
    procedure.addFormalParameter(formalParameter2)
    print("Procedure: " + procedure.toString())
    
    function = Function("F1", "int")
    function.setFrameLength(48)
    function.setStartingQuad("200")
    function.addFormalParameter(formalParameter1)
    function.addFormalParameter(formalParameter2)
    print("Function: " + function.toString())
    