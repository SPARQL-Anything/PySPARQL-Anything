"""
@author Marco Ratta & Enrico Daga
@version 25/01/2023
"""

import pysparql_anything.command as cmd
from pysparql_anything.engine import Engine


class SparqlAnything:
    """
    The class PySparqlAnything provides a Python CLI for the SPARQL Anything
    technology. It replaces the regular command line instructions
    with a call to the run() method.
    It acts as both the client and invoker of the Command class.
    """

    def __init__(self):
        """ Constructor for the class SparqlAnything."""
        self.receiver = Engine()

    def run(self, **kwargs):
        """
        The run method replaces the regular command line execution.
        @param **kwargs The keyword arguments are the same as the regular
            flags for the Sparql Anything CLI, minus the hyphen.
        See the User Guide for an example.
        """
        command = cmd.RunCommand(kwargs, self.receiver)
        command.execute()

    def select(self, **kwargs):
        """
        The select method enables one to run a SELECT query and return
        the result as a Python dictionary.
        @param q The path to the query.
        @return a Python dictionary
        """
        command = cmd.SelectCommand(kwargs, self.receiver)
        return command.execute()

    def ask(self, **kwargs):
        """
        The ask method enables one to run an ASK query and return the result as
        a Python boolean True or False.
        @param q The path to the query
        @param l The RDF file to be queried.
        """
        command = cmd.AskCommand(kwargs, self.receiver)
        return command.execute()

    def construct(self, **kwargs):
        """
        The construct method enables one to run a CONSTRUCT query and
        return the result as a rdflib graph object.
        @param q The path to the query
        @param l The RDF file to be queried.
        """
        command = cmd.ConstructCommand(kwargs, self.receiver)
        return command.execute()
