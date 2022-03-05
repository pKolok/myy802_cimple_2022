"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

import os

class FileParser:
    def __init__(self, filename):
        directory = os.path.dirname(__file__)
        self.filename = os.path.join(directory, "tests", filename)
        self.file = open(self.filename, "r")
        
    def __del__(self):
        self.file.close()
    
    def getNextCharacter(self):
        return self.file.read(1)
    

# test file parser
if __name__ == "__main__":
    print("Testing FileParser ...")
    import sys
    
    filename = sys.argv[1]
    
    fileParser = FileParser(filename)
    char = fileParser.getNextCharacter()
    # while (char != ""):
    while True:
        if (char == "\n"):
            print("new line")
        elif (char == "\t"):
            print("tab")
        elif (char == " "):
            print("space")
        elif (char == ""):
            print("EOF") 
            break
        else:
            print(char)
            
        char = fileParser.getNextCharacter()