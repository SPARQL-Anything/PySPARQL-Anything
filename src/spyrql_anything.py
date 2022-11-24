# The class SpyrqlAnything provides a Python CLI for the SPARQL Anything
# technology. It replaces the regular command line instructions
# with a call to the run() method.
#
# @author Marco Ratta
# @version 23/11/2022 v1.2

import json
import jnius_config

class SpyrqlAnything:

    # Constructor for the class SpyrqlAnything.
    # @param aPath The path to the local .jar file for SPARQL Anything.
    
    def __init__(self, aPath):
        self.reflection = self.reflect(aPath)

    # This method uses Pyjnius to create a reflection of the SPARQLAnything
    # class containing the software's access point (main).
    # @param aPath The path to the local .jar file for SPARQL Anything.
    
    def reflect(self, aPath):
        # JVM configuration:
        jnius_config.set_classpath(aPath)
        # Launch JVM
        from jnius import autoclass
        return autoclass('com.github.sparqlanything.cli.SPARQLAnything')

    # This method replaces the command line execution.
    # @param **kwargs The keyword arguments are the same as the regular
    #                 flags for the Sparql Anything CLI, minus the hyphen.
    #                 See the User Guide for an example.
    
    def run(self, **kwargs):
        if ('f','dict') in kwargs.items():
            kwargs['f'] = 'json'
            kwargs['o'] = 'tmp.json'
            args = buildArgs(kwargs)
            self.reflection.main(args) # Outputs to tmp.json
            with open('tmp.json') as f:
                dictionary = json.load(f)
            return dictionary
        else:    
            args = buildArgs(kwargs)
            if args is None:
                return
            else:
                self.reflection.main(args)
    
    def select(self, **kwargs):
        kwargs['f'] = 'json'
        args = buildArgs(kwargs)
        return json.loads(self.reflection.callMain(args))
        
# Helper for the run method. Constructs the appropriate String array
# to pass to the main method from Python **kwargs.
# @param aDict a Python dictionary.

def buildArgs(aDict):
    # initialises String[]:
    arguments = []
    # Sets -q and its value as the first two elements. Deletes 'q'. 
    if 'q' in aDict:
        arguments.append('-' + 'q')
        arguments.append(aDict['q'])
        aDict.pop('q')
    else:
        print('Invalid argument given. Flag "q" must be passed.')
        return
    # Constructs the rest of arguments.
    for key in aDict.keys():
        arguments.append('-' + key)
        arguments.append(aDict[key])
    # arguments to be passed to the main function. 
    return arguments     
    
