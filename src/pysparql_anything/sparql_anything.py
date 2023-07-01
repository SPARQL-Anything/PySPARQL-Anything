"""
Module containing the SparqlAnything class. This class provides access to
Python users to the functionalities of the SPARQL Anything technology.

@author Marco Ratta
@version 01/07/2023
"""

from rdflib import Graph
import pysparql_anything.command as cmd
from pysparql_anything.sparql_anything_reflection import SparqlAnythingReflection


class SparqlAnything:
    """
    The class SparqlAnything provides access to the SPARQL Anything functions.
    It replaces the regular command line instructions with a call to the run()
    method and provides extra Python specific features.
    """

    def __init__(self, *jvm_options: str):
        """
        Initialiser for the class SparqlAnything.

        Parameters:

        *jvm_options - the options to be passed to the JVM before launch.
        """
        self.receiver = SparqlAnythingReflection(jvm_options)

    def run(self, **kwargs) -> None:
        """
        The run method replaces the regular command line execution.

        Parameters:

        **kwargs - The keyword arguments are the same as those of the regular
        flags for the Sparql Anything CLI, minus the hyphen.
        See the User Guide for an example.
        """
        command = cmd.RunCommand(kwargs, self.receiver)
        command.execute()

    def select(self, **kwargs) -> dict:
        """
        The select method enables one to run a SELECT query and return
        the result as a Python dictionary.

        Parameters:

        **kwargs - The keyword arguments are the same as those of the regular
        flags for the Sparql Anything CLI, minus the hyphen.
        See the User Guide for an example.
        """
        command = cmd.SelectCommand(kwargs, self.receiver)
        return command.execute()

    def ask(self, **kwargs) -> bool:
        """
        The ask method enables one to run an ASK query and return the result as
        a Python boolean True or False.

        Parameters:

        **kwargs - The keyword arguments are the same as those of the regular
        flags for the Sparql Anything CLI, minus the hyphen.
        See the User Guide for an example.
        """
        command = cmd.AskCommand(kwargs, self.receiver)
        return command.execute()

    def construct(self, **kwargs) -> Graph:
        """
        The construct method enables one to run a CONSTRUCT query and
        return the result as a rdflib graph object.

        Parameters:

       **kwargs - The keyword arguments are the same as those of the regular
        flags for the Sparql Anything CLI, minus the hyphen.
        See the User Guide for an example.
        """
        command = cmd.ConstructCommand(kwargs, self.receiver)
        return command.execute()
