"""
@author Marco Ratta
@version 20/01/2023
"""

import jnius_config
from pysparql_anything.config import getPath2Jar


class Engine:
    """
    The class engine wraps the Java SPARQL Anything Main class.
    """

    def __init__(self):
        """ Constructor for the class Engine. """
        self.reflection = self.__reflect()

    def __reflect(self):
        """
        This method uses Pyjnius to create a reflection of the SPARQLAnything
        class containing the software's access point (main).
        @return a reflection of the class SPARQLAnything
        """
        try:
            # JVM configuration
            jnius_config.set_classpath(getPath2Jar())
            # Launch JVM
            from jnius import autoclass, JavaException
            return autoclass('com.github.sparqlanything.cli.SPARQLAnything')
        except ValueError as exception:
            print('Cannot construct two objects for the same VM. \n'
                  + 'Please create a new VM for a new CLI \n')
            print(exception)
        except JavaException as exception:
            # Handles JVM exception for an incorrect path
            print('JVM exception occured: \n'
                  + 'Check the jar has been dowloaded succesfully:\n'
                  + 'try cli.config.isJar() for diagnostic value. \n'
                  + 'CLI must be restarted. \n')
            print(exception)

    def main(self, args):
        """ Wrapper for the SPARQL Anything main method. """
        self.reflection.main(args)

    def callMain(self, args):
        """ Wrapper for the SPARQL Anything callMain method. """
        return self.reflection.callMain(args)
