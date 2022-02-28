"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

# to run from cmd: python compiler.py fibonacci.c

import sys
from FileParser import FileParser

reservedWords = ["program", "declare", "if", "else",  "while", "switchcase",
                 "forcase", "incase", "case", "default", "not", "and", "or",
                 "function", "procedure", "call", "return", "in", "inout", 
                 "input", "print"]
 
class Compiler:
    def __init__(self, filename):
        self.filename = filename
        self.fileParser = FileParser(filename)
        
    def runLexicalAnalyser(self):
        print("Firing lexical analyser ...")
        
        for i in range(20):
            print(self.fileParser.getNextCharacter())
        
        return
        
    def runSyntaxAnalyser(self):
        print("Firing syntax analyser ...")
        return
    
    def runSemanticAnalyser(self):
        return

    def generateIntermediateCode(self):
        return
    
    def optimiseCode(self):
        return
    
    def generateCode(self):
        return
       


    
#print(len(sys.argv))

if len(sys.argv) != 2:
    print("Wrong arguments. Must give just the filename")
    exit(1)

filename = sys.argv[1]
#print(filename)

compiler = Compiler(filename)

compiler.runLexicalAnalyser()

