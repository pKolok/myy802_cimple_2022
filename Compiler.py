"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

from FileParser import FileParser
from LexicalAnalyser import LexicalAnalyser

reservedWords = ["program", "declare", "if", "else",  "while", "switchcase",
                 "forcase", "incase", "case", "default", "not", "and", "or",
                 "function", "procedure", "call", "return", "in", "inout", 
                 "input", "print"]
 
class Compiler:
    def __init__(self, filename):
        self.filename = filename
        self.fileParser = FileParser(filename)
        self.lexicalAnalyser = LexicalAnalyser(self.fileParser)
        
    def runLexicalAnalyser(self):
        
        nextLexicalUnit = self.lexicalAnalyser.getNextLexicalUnit()

        return nextLexicalUnit
        
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
