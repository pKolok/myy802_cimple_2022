"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
"""

import os


class FileParser:
    def __init__(self, filename):
        #self.filename = filename
        directory = os.path.dirname(__file__)
        self.filename = os.path.join(directory, "tests", filename)
        self.file = open(self.filename, "r")
        
    def __del__(self):
        self.file.close()
    
    def getNextCharacter(self):
        return self.file.read(1)