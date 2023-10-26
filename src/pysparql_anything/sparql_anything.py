"""
Module containing the SparqlAnything class. This class provides access to
the functionalities of the SPARQL Anything technology to Python users and
clients.

@author Marco Ratta
@version 23/10/2023
"""

from rdflib import Graph
import pysparql_anything.command as cmd
from pysparql_anything.sparql_anything_reflection import SPARQLAnythingReflection


class SparqlAnything:
    """
    The class SparqlAnything provides a Python interface to the functionalities
    offered by the SPARQL Anything technology.\n
    It replaces the regular SPARQL Anything CLI with a call to the run()
    method and provides extra Python specific features.
    """

    def __init__(self, *jvm_options: str) -> None:
        """
        Initialiser for the class SparqlAnything.\n
        Arguments:\n
        *jvm_options - the options to be passed to the JVM before launch.
        """
        self.receiver = SPARQLAnythingReflection(jvm_options)

    def run(self, **kwargs) -> None:
        """
        The run method replaces the regular command line execution.\n
        Arguments:\n
        **kwargs - The keyword arguments for the RUN request. These are the
            same as those of the regular flags for the Sparql Anything CLI,
            minus the hyphen.\n
            See the User Guide for an example.
        """
        cmd.execute_run(kwargs, self.receiver)

    def select(self, **kwargs) -> dict:
        """
        The select method enables one to run a SELECT query and return
        the result as a Python dictionary.\n
        Arguments:\n
        **kwargs - The keyword arguments for the SELECT request. These are the
            same as those of the regular flags for the Sparql Anything CLI,
            minus the hyphen.\n
            See the User Guide for an example.
        """
        return cmd.execute_select(kwargs, self.receiver)

    def ask(self, **kwargs) -> bool:
        """
        The ask method enables one to run an ASK query and return the result as
        a Python boolean True or False.\n
        Arguments:\n
        **kwargs - The keyword arguments for the ASK request. These are the
            same as those of the regular flags for the Sparql Anything CLI,
            minus the hyphen.\n
            See the User Guide for an example.\n
        """
        return cmd.execute_ask(kwargs, self.receiver)

    def construct(self, **kwargs) -> Graph:
        """
        The construct method enables one to run a CONSTRUCT query and
        return the result as a rdflib graph object.\n
        Parameters:\n
       **kwargs - The keyword arguments for the ASK request. These are the
            same as those of the regular flags for the Sparql Anything CLI,
            minus the hyphen.\n
            See the User Guide for an example.
        """
        return cmd.execute_construct(kwargs, self.receiver)
