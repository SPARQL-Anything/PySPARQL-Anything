# The class PySpyrqlAnything provides a Python CLI for the SPARQL Anything
# technology. It replaces the regular command line instructions
# with a call to the run() method.
#
# @author Marco Ratta & Enrico Daga
# @version 10/01/2023 v1.6

from rdflib import Graph
import json
import jnius_config

class PySparqlAnything:

    # Constructor for the class SpyrqlAnything.
    # @param aPath The path to the local .jar file for SPARQL Anything.
    
    def __init__(self, aPath):
        self.reflection = self.__reflect(aPath)

    # This method uses Pyjnius to create a reflection of the SPARQLAnything
    # class containing the software's access point (main).
    # @param aPath The path to the local .jar file for SPARQL Anything.
    # @return a reflection of the class SPARQLAnything
    
    def __reflect(self, aPath):
        try:
            # JVM configuration
            jnius_config.set_classpath(aPath)
            # Launch JVM
            from jnius import autoclass, JavaException
            return autoclass('com.github.sparqlanything.cli.SPARQLAnything')
        except ValueError as e:
            print('Cannot construct two objects for the same VM. \n'
                  + 'Please create a new VM for a new engine \n' )
            print(e)
        except JavaException as e:
            # Handles JVM exception for an incorrect path
            print('JVM exception occured: check the path passed as input.\n'
                  + 'CLI must be restarted. \n')
            print(e)

    # The run method replaces the regular command line execution.
    # @param **kwargs The keyword arguments are the same as the regular
    #                 flags for the Sparql Anything CLI, minus the hyphen.
    #                 See the User Guide for an example.
    
    def run(self, **kwargs):
        args = buildArgs(kwargs)
        if args is None:
            return
        else:
            self.reflection.main(args)
            
    # The select method enables one to run a SELECT query and return the result
    # as a Python dictionary.
    # @param q The path to the query.
    # @return a Python dictionary
    
    def select(self, **kwargs):
        kwargs['f'] = 'json'
        args = buildArgs(kwargs)
        return json.loads(self.reflection.callMain(args))

    # The ask method enables one to run an ASK query and return the result as
    # a Python boolean True or False.
    # @param q The path to the query
    # @param l The RDF file to be queried.

    def ask(self, **kwargs):
        kwargs['f'] = 'xml'
        args = buildArgs(kwargs)
        string = self.reflection.callMain(args)
        if '<boolean>true</boolean>' in string:
            return True
        else:
            return False
        
    # The construct method enables one to run a CONSTRUCT query and return the
    # result as a rdflib graph object.
    # @param q The path to the query
    # @param l The RDF file to be queried.
    
    def construct(self, **kwargs):
        args = buildArgs(kwargs)
        string = self.reflection.callMain(args)
        g = Graph().parse(data = string)
        return g
        
        
# Helper for the run method. Constructs the appropriate String array
# to pass to the main method from Python **kwargs.
# @param aDict a Python dictionary.
# @return an array of String

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
    
