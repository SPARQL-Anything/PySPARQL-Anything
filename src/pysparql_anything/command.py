"""
This module contains the functions that encapsulate the execution of
each of the commands of the PySPARQL Anything interface.

@author Marco Ratta
@ version 19/10/2023
"""

import json
from rdflib import Graph
from pysparql_anything.parameter_handler import transform_parameters
from pysparql_anything.sparql_anything_reflection import SparqlAnythingReflection


def execute_ask(kwargs: dict, receiver: SparqlAnythingReflection) -> bool:
    '''
    Contains the instructions for the ASK command and executes them.\n
    Arguments: \n
    kwargs - a dictionary containing the SPARQL Anything ASK request parameters.\n
    receiver - a SPARQL Anything reflection object.
    '''
    kwargs['f'] = 'xml'
    args = transform_parameters(kwargs)
    string = receiver.call_main(args)
    return bool('<boolean>true</boolean>' in string)


def execute_construct(kwargs: dict, receiver: SparqlAnythingReflection) -> Graph:
    '''
    Contains the instructions for the CONSTRUCT command and executes them.\n
    Arguments: \n
    kwargs - a dictionary containing the SPARQL Anything CONSTRUCT request parameters.\n
    receiver - a SPARQL Anything reflection object.
    '''
    args = transform_parameters(kwargs)
    string = receiver.call_main(args)
    graph = Graph().parse(data=string)
    return graph


def execute_select(kwargs: dict, receiver: SparqlAnythingReflection) -> dict:
    '''
    Contains the instructions for the SELECT command and executes them.\n
    Arguments: \n
    kwargs - a dictionary containing the SPARQL Anything SELECT request parameters.\n
    receiver - a SPARQL Anything reflection object.
    '''
    kwargs['f'] = 'json'
    args = transform_parameters(kwargs)
    string = receiver.call_main(args)
    return json.loads(string)


def execute_run(kwargs: dict, receiver: SparqlAnythingReflection) -> None:
    '''
    Contains the instructions for the RUN command and executes it.\n
    Arguments: \n
    kwargs - a dictionary containing the SPARQL Anything RUN request parameters.\n
    receiver - a SPARQL Anything reflection object.
    '''
    args = transform_parameters(kwargs)
    receiver.main(args)
