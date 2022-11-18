# The class SpyrqlAnything provides a Python CLI for the SPARQL Anything
# technology. It replaces the regular command line instructions
# with a call to the run() method.
#
# @author Marco Ratta
# @version 17/11/2022

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
    # @param args The arguments required by the SPARQL Anything query as
    #             defined in the SPARQL Anything specification. NOTE that
    #             the flags and their values need to be passed as separate
    #             strings.
    
    def run(self, args):
        self.reflection.main(args)
    
