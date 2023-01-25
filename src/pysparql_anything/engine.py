"""
@author Marco Ratta
@version 24/01/2023
"""

import jnius_config
from pysparql_anything.config import get_path2jar


class Engine:
    """
    The class engine wraps the Java SPARQL Anything Main class.
    Acts as the receiver of the Command pattern.
    """

    def __init__(self):
        """ Constructor for the class Engine. """
        self.reflection = self.__reflect()

    def __reflect(self):
        """
        This method uses Pyjnius to create a reflection of the SPARQLAnything
        class containing the software's access point (main).
        @return a reflection of the class SPARQLAnything
        @raises ValueError and JavaException
        """
        try:
            # JVM configuration
            jnius_config.set_classpath(get_path2jar())
            # Launch JVM
            from jnius import autoclass, JavaException
            return autoclass('com.github.sparqlanything.cli.SPARQLAnything')
        except ValueError:
            print('Cannot construct two objects for the same VM. \n'
                  + 'Please exit and restart the Python environment and '
                  + 'create a new VM for the  CLI.')
            raise
        except JavaException:
            # Handles JVM exception for an incorrect path
            print('JVM exception occured: \n'
                  + 'Check that the jar has been dowloaded successfully:\n'
                  + 'try cli.config.has_jar() for a diagnostic value. \n'
                  + 'Python environment must be exited and restarted \n'
                  + 'for a new JVM to be launched.')
            raise

    def main(self, args):
        """ Wrapper for the SPARQL Anything main method. """
        self.reflection.main(args)

    def call_main(self, args):
        """ Wrapper for the SPARQL Anything callMain method. """
        return self.reflection.callMain(args)
