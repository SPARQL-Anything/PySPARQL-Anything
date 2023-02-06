"""
@author Marco Ratta & Enrico Daga
@version 05/02/2023
"""

import pysparql_anything.command as cmd
from pysparql_anything.engine import Engine
from  pysparql_anything.invoker import Invoker


class SparqlAnything:
    """ The class PySparqlAnything provides a Python CLI for the SPARQL
    Anything technology.
    It replaces the regular command line instructions with a call to the
    run() method.
    Acts as the client of the Command pattern.
    """

    def __init__(self):
        """ Constructor for the class SparqlAnything."""
        self.receiver = Engine()
        self.invoker = Invoker()

    def run(self, **kwargs):
        """
        The run method replaces the regular command line execution.
        """
        command = cmd.RunCommand(kwargs, self.receiver)
        self.invoker.set_command(command)
        return self.invoker.run_query()

    def select(self, **kwargs):
        """ The select method enables one to run a SELECT query and return
        the result as a Python dictionary.
        """
        command = cmd.SelectCommand(kwargs, self.receiver)
        self.invoker.set_command(command)
        return self.invoker.run_query()

    def ask(self, **kwargs):
        """ The ask method enables one to run an ASK query and return the result as
        a Python boolean True or False.
        """
        command = cmd.AskCommand(kwargs, self.receiver)
        self.invoker.set_command(command)
        return self.invoker.run_query()

    def construct(self, **kwargs):
        """ The construct method enables one to run a CONSTRUCT query and
        return the result as a rdflib graph object.
        """
        command = cmd.ConstructCommand(kwargs, self.receiver)
        self.invoker.set_command(command)
        return self.invoker.run_query()
