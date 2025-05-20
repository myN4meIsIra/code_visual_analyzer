# script details
"""
object that holds information about the script
~ Ira Garrett
"""

class ScriptDetails:

    def __init__(self):
        self.functions = []
        self.functionConnections = []
        self.imports = []
        self.vars = []
        self.blockComments = []
        self.lineComments = []


    ''' populate the obj '''
    def populateDetails(self,
                        functions,
                        functionConnections,
                        imports,
                        vars,
                        blockComments,
                        lineComments,
                        ):
        self.functions = functions
        self.functionConnections = functionConnections
        self.imports = imports
        self.vars = vars
        self.blockComments = blockComments
        self.lineComments = lineComments

        return self

    ''' add a function to the list '''
    def addFunction(self, functionName):
        self.functions.append(functionName)
        return self

    ''' add a function association to the list'''
    def addFunctionConnection(self, function1, function2):
        self.functionConnections.append([function1, function2])

    ''' get obj '''
    def getDetails(self):
        return self
