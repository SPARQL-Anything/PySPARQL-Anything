"""
@author Marco Ratta
@ version 19/10/2023
"""

import json
from rdflib import Graph
from pysparql_anything.parameter_handler import transform_parameters
from pysparql_anything.sparql_anything_reflection import SparqlAnythingReflection


def execute_ask(kwargs: dict, receiver: SparqlAnythingReflection) -> bool:
    kwargs['f'] = 'xml'
    args = transform_parameters(kwargs)
    string = receiver.call_main(args)
    return bool('<boolean>true</boolean>' in string)


def execute_construct(kwargs: dict, receiver: SparqlAnythingReflection) -> Graph:
    args = transform_parameters(kwargs)
    string = receiver.call_main(args)
    graph = Graph().parse(data=string)
    return graph


def execute_select(kwargs: dict, receiver: SparqlAnythingReflection) -> dict:
    kwargs['f'] = 'json'
    args = transform_parameters(kwargs)
    string = receiver.call_main(args)
    return json.loads(string)


def execute_run(kwargs: dict, receiver: SparqlAnythingReflection) -> None:
    args = transform_parameters(kwargs)
    receiver.main(args)
