# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 20:37:00 2022

@author: panou
"""

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
        for quad in self.quads:
            if quad.label in list:
                quad.result = label
        return
    
    def print(self):
        for quad in self.quads:
            print(quad.toString())
    

# test Intermediate code
if __name__ == "__main__":
    
    # test Quad
    quad = Quad("100", "+", "x", "1", "y")
    print(quad.toString())
    
    # test IntermediateCode
    engine = IntermediateCode()
    x1 = engine.makeList(engine.nextQuad())
    quad1 = engine.genQuad('jump','_','_','_')
    quad2 = engine.genQuad('+','a','1','a')
    x2 = engine.makeList(engine.nextQuad())
    quad3 = engine.genQuad('jump','_','_','_')
    x = engine.mergeList(x1,x2)
    quad4 = engine.genQuad('+','a','2','a')
    
    print("Before:")
    engine.print()
    
    engine.backpatch(x,engine.nextQuad())
    
    print("After:")
    engine.print()