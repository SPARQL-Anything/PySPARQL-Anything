"""
This module contains the SparqlAnything class. This class provides a Python
based API access to the functionalities of the SPARQL Anything tool.

Author: Marco Ratta
Date: 20/06/2025
"""

from typing import Any
import rdflib
import pandas as pd
import networkx as nx
from pysparql_anything.executor import Executor
from pysparql_anything.sparql_anything_reflection import (
    SPARQLAnythingReflection
)


class Singleton(type):
    """
    The Singleton metaclass specifies the routine for instantiating a
    SparqlAnything object according to a Singleton pattern. This has been
    made necessary by the limitations of the JNI.
    """
    _instance = None

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls._instance is None:
            # Here the new and init methods of SparqlAnything are called:
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance
        return cls._instance


class SparqlAnything(metaclass=Singleton):
    """
    The class SparqlAnything provides a Python interface to the functionalities
    offered by the SPARQL Anything tool.\n
    Args:\n
        *jvm_options - the optional arguments to be passed to the JVM
            before launch.
    """
    def __init__(self, *jvm_options: str) -> None:
        self.executor = Executor(
            SPARQLAnythingReflection(jvm_options)
        )

    def run(self, **kwargs: str | dict[str, str]) -> None:
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
        self.executor.execute_run(kwargs)

    def select(
            self, output_type: type = dict, **kwargs: str | dict[str, str]
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
        return self.executor.execute_select(kwargs, output_type)

    def ask(self, **kwargs: str | dict[str, str]) -> bool:
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
        return self.executor.execute_ask(kwargs)

    def construct(
        self,
        graph_type: type = rdflib.Graph,
        **kwargs: str | dict[str, str]
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
        return self.executor.execute_construct(kwargs, graph_type)
