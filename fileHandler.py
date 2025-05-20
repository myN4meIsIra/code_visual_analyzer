# file handler
"""
handle how files are worked with
Ira Garrett 5-19-25
"""

# imports
from matplotlib.pyplot import figtext


# custom imports
from scriptDetails import ScriptDetails


class FileHandler:

    # initialization
    """
    on init, get the file we want to pull data from
    """
    def __init__(self):
        import os
        files = os.listdir('.')

        # Print each filename
        for fileNum in range(len(files)):
            if ".py" in files[fileNum]:
                print(f"{fileNum} {files[fileNum]}")

        #self.fileName = files[3]
        self.fileName = files[int(input("please enter the number for the file you would like to analyze"))]


    # pull file
    """
        pull a file for analysis, returning the contents of the file as an array
    """
    def pullFile(self):
        print(f'file {self.fileName} text:')
        fileText = []
        with open(self.fileName, 'r') as file:
            for line in file:
                print(line)
                if line  != '\n': fileText.append(line)

        return fileText


    # analyze code
    """
        iterate over lines, running various analysis scripts to determine associations and interesting things about he code
        @code: an array of text, containing python code to be analyzed
    """
    def analyzeCode(self, code):
        # imports
        import networkx as nx
        import matplotlib.pyplot as plt
        import re

        # instantiate ScriptDetails
        scriptDetails = ScriptDetails()

        # local vars
        current_function = ''
        script_name = self.fileName

        # Create a directed graph for function dependencies
        function_connections= nx.DiGraph()

        # print the number of lines of code
        print(f'length of the script: {len(code)} lines')

        # iterate over the lines of code
        for line in code:
            print(f' line: {line}')

            # define/update details
            imports = scriptDetails.imports
            functions = scriptDetails.functions
            vars = scriptDetails.vars

            # analysis logic
            function = re.search("def.*\(.*", line)
            import_statement = re.search("import", line)
            comment_line = re.search("#", line)                         #unused
            block_comment = re.search("\'\'\'|\"\"\"",line)             #unused
            variable = re.search("^.*[^=, ^!, ^\-, ^+]=[^=].*$", line)  #unused

            update_current_function = re.search("^def.*\(.*", line)
            function_call = re.search("[a-z|A-Z]*\(.*\)", line)



            ''' handlers for analysis logic '''

            # if there is an import statement
            if import_statement:
                try:
                    # perform logic and str manipulation to get the imported function's name from the line
                    importLine = line
                    import_line_array = importLine.split()

                    for i in range(len(import_line_array)):
                        if i == 0 and import_line_array[i] == "import":
                            importLine = importLine.strip("\n")
                            import_line_array2 = importLine.split('import')
                            importLine = import_line_array2[-1]

                            # handle for nested imports
                            if importLine != import_line_array2[-1]:
                                importLine += f"->{import_line_array2[1:]}"

                            # add it to the list
                            imports.append(importLine)

                            # create visual stuffs for it
                            function_connections.add_node(importLine, color="green")
                            function_connections.add_edge(script_name, importLine, color='green')
                except:
                    print(f'failure with handling import line {line}')


            # if there is a function statement -- a function definition statement
            if function:
                # perform str manipulation to get the function name
                current_function = line.split()[1].split('(')[0]
                try:
                    function_name = line
                    function_name_array = function_name.split('(')
                    function_name = function_name_array[0]
                    if re.search('def', function_name):
                        function_name_array2 = function_name.split('def')
                        function_name = function_name_array2[1]

                        # add it to the list
                        functions.append(function_name)

                        # graphical stuffs
                        function_connections.add_node(function_name, color="blue")
                        function_connections.add_edge(script_name, function_name, color='blue')
                except:
                    pass

            # record connections between functions
            if update_current_function:
                try:
                    # add it to the list
                    current_function = function_name
                    functions = scriptDetails.getDetails().functions
                    if function_name not in functions:
                        scriptDetails.addFunction(function_name)
                except:
                    pass

            if function_call and not update_current_function:
                try:
                    # perform string manipulation
                    function_call_name = line
                    function_call_name = function_call_name.split('=')[-1]
                    function_call_name = function_call_name.split('(')[0]
                    function_call_name = function_call_name.split("def")[-1]

                    # add it to the list
                    if function_call_name not in functions:
                        scriptDetails.addFunction(function_call_name)
                    scriptDetails.addFunctionConnection(current_function, function_call_name)

                except:
                    pass

        # iterate over the functions that have connections, and create the visulas for them
        function_connectionsList = scriptDetails.getDetails().functionConnections
        for i in function_connectionsList:
            print(f"i = {i}")
            function_connections.add_node(str(i[0]), color="yellow")
            function_connections.add_edge(str(i[0]), str(i[1]), color='yellow')

        print(f"imports: {imports}")
        print(f"vars: {vars}")
        print(f"current function: {current_function}")
        print(f"functions: {functions}")


        # handle for the plot and graphics stuffs
        ''' graphics stuffs '''
        for node in function_connections.nodes():
            if "color" not in function_connections.nodes[node]:
                function_connections.nodes[node]["color"] = "gray"  # Default color

        node_colors = [function_connections.nodes[node]["color"] for node in function_connections.nodes()]
        edge_colors = [function_connections.edges[edge]["color"] for edge in function_connections.edges()]

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(function_connections)  # Layout for positioning nodes
        nx.draw(function_connections, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, font_weight="bold",
                edge_cmap=plt.cm.Blues)
        plt.show()

