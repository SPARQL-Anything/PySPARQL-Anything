"""
@author Marco Ratta
@ version 05/02/2023
"""

import json
from typing import Protocol
from rdflib import Graph
from pysparql_anything.parameter_handler import ParameterHandler
from pysparql_anything.engine import Engine


class Command(Protocol):
    """ Protocol to define the interface of a command request. """

    def execute(self):
        """ Execute method to be overridden by the implementing classes. """


class AskCommand:
    """ Implements the Command protocol for an ASK request. """

    def __init__(self, kwargs: dict, receiver: Engine):
        """ Initialiser for the AskCommand concrete class. """
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self) -> bool:
        """ Instructions for an ASK request. """
        self.handler.set_format('xml')
        args = self.handler.combine()
        string = self.receiver.call_main(args)
        return bool('<boolean>true</boolean>' in string)


class ConstructCommand:
    """ Implements the Command protocol for a CONSTRUCT request. """

    def __init__(self, kwargs: dict, receiver: Engine):
        """ Initialiser for the ConstructCommand concrete class. """
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self) -> Graph:
        """ Instructions for a CONSTRUCT request. """
        args = self.handler.combine()
        string = self.receiver.call_main(args)
        graph = Graph().parse(data=string)
        return graph


class SelectCommand:
    """ Implements the Command protocol for a SELECT request. """

    def __init__(self, kwargs: dict, receiver: Engine):
        """ Initialiser for the SelectCommand concrete class."""
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self) -> dict:
        """ Instructions for a SELECT request. """
        self.handler.set_format('json')
        args = self.handler.combine()
        string = self.receiver.call_main(args)
        return json.loads(string)


class RunCommand:
    """ Implements the Command protocol for a RUN request. """

    def __init__(self, kwargs: dict, receiver: Engine):
        """ Initialiser for the RunCommand concrete class. """
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self) -> None:
        """ Instructions for a RUN request. """
        args = self.handler.combine()
        self.receiver.main(args)