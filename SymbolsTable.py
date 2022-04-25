"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

from abc import ABC,abstractmethod

class SymbolsTable:
    
    def __init(self):
        self.scopes = []
    
    def addScope(self, scopeName):
        self.scopes.append(Scope(scopeName))
        
    def removeScope(self):
        self.scopes.pop()
    
class Scope:
    
    def _init(self, name):
        self.name = name
        self.index = 1
    

class Entity(ABC):
    
    # def __init__(self, name):
    #     self.name = name

    @property
    @abstractmethod
    def name(self):
        pass


class Variable(Entity):
    
    def __init__(self, name, datatype, offset):
        self.name = name
        self.datatype = datatype
        self.offset = offset
    
    @property
    def name(self):
        return self.name
    
class TemporaryVariable(Variable):
    
    def __init__(self, name, datatype, offset):
        self.name = name
        self.datatype = datatype
        self.offset = offset
        
# The parameters which appear in a function/procedure declaration
class FormalParameter(Entity):
    
    def __init__(self, name, datatype, mode):
        self.name = name
        self.datatype = datatype
        self.mode = mode
    
    @property
    def name(self):
        return self.name
        
class Parameter(FormalParameter):
    
    def __inti__(self, name, datatype, mode, offset):
        self.name = ""          # not necessary but for consistency
        self.datatype = ""
        self.mode = ""
        self.offset = ""
        
    @property
    def name(self):
        return self.name
    
class Procedure(Entity):
    
    def __init__(self):
        self.name = ""
        self.startingQuad = ""
        self.frameLength = ""
        self.formalParameters = []
    
    @property
    def name(self):
        return self.name
    
    def setStartingQuad(self, quad):
        self.startingQuad = quad
        
class Function(Procedure):
    
    def __init__(self):
        self.name = ""
        self.datatype = ""
        self.startingQuad = ""
        self.frameLength = ""
        self.formalParameters = []
        
    def setStartingQuad(self, quad):
        self.startingQuad = quad
        
class SumbolicConstant(Entity):
    
    def __init__(self):
        self.name = ""
        self.value = ""