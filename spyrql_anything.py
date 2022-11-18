# The class SpyrqlAnything provides a Python CLI for the SPARQL Anything
# technology. It replaces the regular command line instructions
# with a call to the run() method.
#
# @author Marco Ratta
# @version 18/11/2022 v1.1

class SpyrqlAnything:

    # Constructor for the class SpyrqlAnything.
    # @param aPath The path to the local .jar file for SPARQL Anything.
    
    def __init__(self, aPath):
        self.reflection = self.reflect(aPath)

    # This method uses Pyjnius to create a reflection of the SPARQLAnything
    # class containing the software's access point (main).
    # @param aPath The path to the local .jar file for SPARQL Anything.
    
    def reflect(self, aPath):
        import jnius_config
        jnius_config.set_classpath(aPath)
        from jnius import autoclass
        return autoclass('com.github.sparqlanything.cli.SPARQLAnything')

    # This method replaces the command line execution.
    # @param **kwargs The keyword arguments are the same as the regular
    #                 flags for the Sparql Anything CLI, minus the hyphen.
    #                 See the User Guide for an example.
    
    def run(self, **kwargs):
        args = buildArgs(kwargs)
        if args is None:
            return
        else:
            self.reflection.main(args)

# Helper for the run method. Constructs the appropriate String array
# to pass to the main method from Python **kwargs.
# @param aDict a Python dictionary.

def buildArgs(aDict):
    # initialises String[]:
    arguments = [] 
    # Sets -q and its value as the first two elements.
    for key in aDict.keys():
        if key == 'q':
            arguments.append('-' + key)
            arguments.append(aDict[key])
    if len(arguments) == 0:
        print('Invalid argument given. Flag "q" must be passed.')
        return
    else: # Deletes the 'q' entry from kwargs.
        aDict.pop('q') 
    # Constructs the rest of arguments.
    for key in aDict.keys():
        arguments.append('-' + key)
        arguments.append(aDict[key])
    # arguments to be passed to the main function. 
    return arguments     
    
