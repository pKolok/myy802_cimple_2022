"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

# to run from cmd: python cimple.py fibonacci.c

import sys
from Compiler import Compiler
  
if len(sys.argv) != 2:
    print("Wrong arguments. Must give just the filename")
    sys.exit()

filename = sys.argv[1]


compiler = Compiler(filename)

lexicalUnit = compiler.runLexicalAnalyser()
while (lexicalUnit != "."):
    print(lexicalUnit)
    lexicalUnit = compiler.runLexicalAnalyser()
print(lexicalUnit)
