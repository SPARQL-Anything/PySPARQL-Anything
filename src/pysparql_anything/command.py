"""
This module contains the functions that encapsulate the execution of
each of the commands of the PySPARQL Anything interface.

Author: Marco Ratta
Date: 06/03/2024
"""

import json
from rdflib import Graph
import networkx as nx
import pandas as pd
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
from pysparql_anything.args_handlers import transform_args
from pysparql_anything.sparql_anything_reflection import SPARQLAnythingReflection


# Helpers for the command execution functions.
def to_pandas_df(select_dict: dict) -> pd.DataFrame:
    """
    Helper method to convert the sa.SparqlAnything.select method's dictonary
    result of a SELECT query into a corresponding pandas DataFrame object.\n
    Args:\n
        select_dict: The dictionary containing the SELECT query results.\n
    Returns:\n
        A pandas DataFrame of the bindings.
    """
    data = []
    columns = select_dict["head"]["vars"]
    bindings = select_dict["results"]["bindings"]
    for binding in bindings:
        row = []
        for column in columns:
            result = binding.get(column, "None")
            if result != "None":
                row.append(result["value"])
            else:
                row.append(result)
        data.append(row)
    return pd.DataFrame(data, columns=columns)


# Command execution functions.
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
    kwargs["format"] = "xml"
    args = transform_args(kwargs)
    string = receiver.call_main(args)
    return bool('<boolean>true</boolean>' in string)


def execute_construct(
        kwargs: dict, receiver: SPARQLAnythingReflection, graph_type: type
        ) -> Graph | nx.MultiDiGraph:
    """
    Contains the instructions for the CONSTRUCT command and executes them.\n
    Args: \n
        kwargs: A dictionary containing the SPARQL Anything CONSTRUCT request
            parameters.\n
        receiver: A SPARQLAnythingReflection object.\n
        graph_type: The type of graph to be returned.
            Either rdflib.Graph or nx.MultiDiGraph.\n
    Returns:
        A rdflib.Graph or nx.MultiDiGraph object.
    """
    args = transform_args(kwargs)
    string = receiver.call_main(args)
    graph = Graph().parse(data=string)
    if graph_type == nx.MultiDiGraph:
        return rdflib_to_networkx_multidigraph(graph)
    return graph


def execute_select(
        kwargs: dict, receiver: SPARQLAnythingReflection, output_type: type
        ) -> dict | pd.DataFrame:
    """
    Contains the instructions for the SELECT command and executes them.\n
    Args: \n
        kwargs: a dictionary containing the SPARQL Anything SELECT request
            parameters.\n
        receiver: a SPARQL Anything reflection object.\n
        output_type: The type of object to return.
            Either dict or pd.DataFrame.\n
    Returns: \n
        A Python dict or a pd.DataFrame containing the results of the
            SELECT query.
    """
    kwargs["format"] = "json"
    args = transform_args(kwargs)
    string = receiver.call_main(args)
    results_dict = json.loads(string)
    if output_type == dict:
        return results_dict
    return to_pandas_df(results_dict)


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
