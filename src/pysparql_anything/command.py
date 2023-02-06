"""
@author Marco Ratta
@ version 05/02/2023
"""

import json
from typing import Protocol, TypeVar, Any
from rdflib import Graph
from pysparql_anything.parameter_handler import ParameterHandler
from pysparql_anything.engine import Engine

# Type aliases
Engine = TypeVar('Engine', bound=Engine)
RdflibGraph = TypeVar('RdflibGraph', bound=Graph)


class Command(Protocol):
    """ Protocol to define the interface of a command request"""

    def execute(self) -> Any:
        """ Execute method to be overridden by the implementing calsses"""


class AskCommand:
    """ Implements the Command protocol for an ask request """

    def __init__(self, kwargs: dict, receiver: Engine):
        """ Constructor for the AskCommand concrete class."""
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self) -> bool:
        """ instructions for an ask request """
        self.handler.set_format('xml')
        args = self.handler.combine()
        string = self.receiver.call_main(args)
        return bool('<boolean>true</boolean>' in string)


class ConstructCommand:
    """ Implements the Command class for a construct request """

    def __init__(self, kwargs: dict, receiver: Engine):
        """ Constructor for the ConstructCommand concrete class."""
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self) -> RdflibGraph:
        """ instructions for a construct request """
        args = self.handler.combine()
        string = self.receiver.call_main(args)
        graph = Graph().parse(data=string)
        return graph


class SelectCommand:
    """ Implements the Command class for a select request """

    def __init__(self, kwargs: dict, receiver: Engine):
        """ Constructor for the SelectCommand concrete class."""
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self) -> dict:
        """ instructions for a select request """
        self.handler.set_format('json')
        args = self.handler.combine()
        string = self.receiver.call_main(args)
        return json.loads(string)


class RunCommand:
    """ Implements the Command class for a run request """

    def __init__(self, kwargs: dict, receiver: Engine):
        """ Constructor for the RunCommand concrete class."""
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self) -> None:
        """ instructions for a run request """
        args = self.handler.combine()
        self.receiver.main(args)
