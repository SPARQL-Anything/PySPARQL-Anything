"""
This module contains the functions that encapsulate the execution of
each of the commands of the PySPARQL Anything interface.

Author: Marco Ratta
Version: 29/02/2024
"""

import json
from rdflib import Graph
import networkx as nx
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
from pysparql_anything.args_handlers import transform_args
from pysparql_anything.sparql_anything_reflection import SPARQLAnythingReflection


def execute_ask(kwargs: dict, receiver: SPARQLAnythingReflection) -> bool:
    """
    Contains the instructions for the ASK command and executes them.\n
    Args: \n
        kwargs: A dictionary containing the SPARQL Anything ASK request
            parameters.\n
        receiver: A SPARQLAnythingreflection object.\n
    Returns:\n
        A boolean True or False.
    """
    kwargs['f'] = 'xml'
    args = transform_args(kwargs)
    string = receiver.call_main(args)
    return bool('<boolean>true</boolean>' in string)


def execute_construct(
        kwargs: dict, receiver: SPARQLAnythingReflection, graph_type: str
        ) -> Graph | nx.MultiDiGraph:
    """
    Contains the instructions for the CONSTRUCT command and executes them.\n
    Args: \n
        kwargs: A dictionary containing the SPARQL Anything CONSTRUCT request
            parameters.\n
        graph_type: The type of graph to be returned. Either "rdflib.Graph" or
            "nx.MultiDiGraph".\n
        receiver: A SPARQLAnythingReflection object.\n
    Returns:
        A rdflib.Graph or nx.MultiDiGraph object.
    """
    args = transform_args(kwargs)
    string = receiver.call_main(args)
    graph = Graph().parse(data=string)
    if graph_type == "nx.MultiDiGraph":
        return rdflib_to_networkx_multidigraph(graph)
    return graph


def execute_select(kwargs: dict, receiver: SPARQLAnythingReflection) -> dict:
    """
    Contains the instructions for the SELECT command and executes them.\n
    Args: \n
        kwargs: a dictionary containing the SPARQL Anything SELECT request
            parameters.\n
        receiver: a SPARQL Anything reflection object.\n
    Returns: \n
        A Python dict containing the results of the SELECT query.
    """
    kwargs['f'] = 'json'
    args = transform_args(kwargs)
    string = receiver.call_main(args)
    return json.loads(string)


def execute_run(kwargs: dict, receiver: SPARQLAnythingReflection) -> None:
    """
    Contains the instructions for the RUN command and executes it.\n
    Args: \n
        kwargs: a dictionary containing the SPARQL Anything RUN request
            parameters.\n
        receiver: a SPARQL Anything reflection object.
    """
    args = transform_args(kwargs)
    receiver.main(args)
    return None
