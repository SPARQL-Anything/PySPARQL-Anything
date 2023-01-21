"""
@author Marco Ratta & Enrico Daga
@version 21/01/2023
"""

import json
from rdflib import Graph
from pysparql_anything.engine import Engine
from pysparql_anything.parameters import Parameters


class SparqlAnything:
    """
    The class PySparqlAnything provides a Python CLI for the SPARQL Anything
    technology. It replaces the regular command line instructions
    with a call to the run() method.
    """

    def __init__(self):
        """ Constructor for the class SparqlAnything."""
        self.engine = Engine()  # Connects to SPARQL Anything

    def run(self, **kwargs):
        """
        The run method replaces the regular command line execution.
        @param **kwargs The keyword arguments are the same as the regular
            flags for the Sparql Anything CLI, minus the hyphen.
        See the User Guide for an example.
        """
        args = Parameters().makeArgs(kwargs)
        if args is not None:
            self.engine.main(args)

    def select(self, **kwargs):
        """
        The select method enables one to run a SELECT query and return
        the result as a Python dictionary.
        @param q The path to the query.
        @return a Python dictionary
        """
        kwargs['f'] = 'json'
        args = Parameters().makeArgs(kwargs)
        return json.loads(self.engine.callMain(args))

    def ask(self, **kwargs):
        """
        The ask method enables one to run an ASK query and return the result as
        a Python boolean True or False.
        @param q The path to the query
        @param l The RDF file to be queried.
        """
        kwargs['f'] = 'xml'
        args = Parameters().makeArgs(kwargs)
        string = self.engine.callMain(args)
        return bool('<boolean>true</boolean>' in string)

    def construct(self, **kwargs):
        """
        The construct method enables one to run a CONSTRUCT query and
        return the result as a rdflib graph object.
        @param q The path to the query
        @param l The RDF file to be queried.
        """
        args = Parameters().makeArgs(kwargs)
        string = self.engine.callMain(args)
        graph = Graph().parse(data=string)
        return graph
