"""
This module contains the SparqlAnything class. This class provides a Python
based API access to the functionalities of the SPARQL Anything tool.

Author: Marco Ratta
Date: 06/03/2024
"""

import rdflib
import pandas as pd
import networkx as nx
import pysparql_anything.command as cmd
from pysparql_anything.sparql_anything_reflection import SPARQLAnythingReflection


class SparqlAnything:
    """
    The class SparqlAnything provides a Python interface to the functionalities
    offered by the SPARQL Anything tool.\n
    Args:\n
        *jvm_options - the optional arguments to be passed to the JVM
            before launch.
    """
    def __init__(self, *jvm_options: str) -> None:
        self.receiver = SPARQLAnythingReflection(jvm_options)

    def run(self, **kwargs) -> None:
        """
        The run method allows the user to run a SPARQL query within a Python
        shell or within a Python script and either have the results printed to
        standard out or save them to a file.\n
        Args:\n
            **kwargs: The keyword arguments for the RUN request. These are the
                same as those of the regular flags for the Sparql Anything CLI,
                minus the hyphen.\n
                See the User Guide for an example.\n
        """
        cmd.execute_run(kwargs, self.receiver)

    def select(
            self, output_type: type = dict, **kwargs
            ) -> dict | pd.DataFrame:
        """
        The select method enables one to run a SELECT query and return
        the result as either a Pandas DataFrame or a Python dictionary.\n
        Args:\n
            output_type: pandas.DataFrame or dict for the chosen output.\n
            **kwargs: The keyword arguments for the SELECT request. These are
                the same as those of the regular flags for the Sparql Anything
                CLI, minus the hyphen.\n
                See the User Guide for an example.\n
        Returns: \n
            A Python dict containing the results of the SELECT query.\n
        Raises:
            ValueError if output_type is not one of the two specified above.
        """
        output_types = [dict, pd.DataFrame]
        if output_type not in output_types:
            raise ValueError(
                "Invalid output type. Expected one of: %s" % output_types
            )
        return cmd.execute_select(kwargs, self.receiver, output_type)

    def ask(self, **kwargs) -> bool:
        """
        The ask method enables one to run an ASK query and return the result as
        a Python boolean True or False.\n
        Args:\n
            **kwargs: The keyword arguments for the ASK request. These are the
                same as those of the regular flags for the Sparql Anything CLI,
                minus the hyphen.\n
                See the User Guide for an example.\n
        Returns:\n
            A Python True/False.
        """
        return cmd.execute_ask(kwargs, self.receiver)

    def construct(
            self, graph_type: type = rdflib.Graph, **kwargs
            ) -> rdflib.Graph | nx.MultiDiGraph:
        """
        The construct method enables one to run a CONSTRUCT query and
        return the result as either a rdflib or networkx MultiDiGraph
        graph object.\n
        Args:\n
            graph_type: The type specifying which graph object is to be
                returned. Default is rdflib.Graph. Alternative is
                networkx.MultiDiGraph.\n
            **kwargs: The keyword arguments for the ASK request. These are the
                same as those of the regular flags for the Sparql Anything CLI,
                minus the hyphen.\n
                See the User Guide for an example.\n
        Returns:\n
            A rdflib.Graph or nx.MultiDiGraph object.\n
        Raises:
            ValueError if graph_type is not one of the two specified above.
        """
        graph_types = [rdflib.Graph, nx.MultiDiGraph]
        if graph_type not in graph_types:
            raise ValueError(
                "Invalid graph type. Expected one of: %s" % graph_types
            )
        return cmd.execute_construct(kwargs, self.receiver, graph_type)
