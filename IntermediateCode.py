"""
Name:       PANAGIOTIS KOLOKOURIS
AM:         4914
Username:   cse94914
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
    
    def toC(self):
        
        if self.operator in ["begin_block", "end_block"]:
            cCode = "L_" + self.label + ":"
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if self.operator == "halt":
            cCode = "L_" + self.label + ": return(0);"
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == ":="):
            cCode = ("L_" + self.label + ": " + self.result + "=" + self.arg1 
                    + ";")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator in ["+", "-", "*", "/"]):
            cCode = ("L_" + self.label + ": " + self.result + "=" 
                    + self.arg1 + self.operator + self.arg2 + ";")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == "="):
            cCode = ("L_" + self.label + ": if (" + self.arg1 + "==" 
                    + self.arg2 + ") goto L_" + self.result + ";")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator in [">", "<", "<>", ">=", "<="]):
            cCode = ("L_" + self.label + ": if (" + self.arg1 + self.operator 
                    + self.arg2 + ") goto L_" + self.result + ";")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == "jump"):
            cCode = ("L_" + self.label + ": goto L_" + self.result + ";")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == "in"):
            cCode = ("L_" + self.label + ": scanf(%d, &" + self.arg1 + ");")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == "out"):
            cCode = ("L_" + self.label + ": printf(%d, " + self.arg1 + ");")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        if (self.operator == "ret"):
            cCode = ("L_" + self.label + ":return(" + self.arg1 + ");")
            comment = "// " + self.toString()
            return (f"{cCode : <35}{comment : <30}")
        
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
        for l in list:
            self.quads[int(l)-100].result = label
        return
    
    def print(self):
        for quad in self.quads:
            print(quad.toString())
            
    def saveToFile(self):
        file = open("test.int", "w")
        for quad in self.quads:
            file.write(quad.toString() + "\n")
        file.close()
        
    def convertToC(self):
        cLines = ["int main()", "{"]
        
        # Collect variables
        variables = self.__discoverVariables()
        if (len(variables) == 0):
            return
        
        variableLine = "int "
        for var in variables:
            variableLine += var + ","
        variableLine = variableLine[:-1] + ";"
        cLines.append(variableLine)
        
        # Construct remaining c lines
        for quad in self.quads:
            cLines.append(quad.toC())
        
        # Save to file
        file = open("test.c", "w")
        for line in cLines:
            file.write(line + "\n")
        file.close()

    def __discoverVariables(self):
        variables = set()
        
        for quad in self.quads:
            
            # if function/procedure is discovered -> exit
            if quad.operator == "par":
                return set()
            
            # skip some lines entirely
            if quad.operator in ["begin_block", "end_block", "halt", "jump"]:
                continue
            
            # everything which is not a number or "_" is a variable
            if (not quad.arg1.isdigit() and quad.arg1 != "_"):
                variables.add(quad.arg1)
            if (not quad.arg2.isdigit() and quad.arg2 != "_"):
                variables.add(quad.arg2)
            if (not quad.result.isdigit() and quad.result != "_"):
                variables.add(quad.result)

        return variables
    
    
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