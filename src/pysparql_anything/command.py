"""
@author Marco Ratta
@ version 02/02/2023
"""

import json
from abc import ABC, abstractmethod
from rdflib import Graph
from pysparql_anything.parameter_handler import ParameterHandler


class Command(ABC):
    """
    Abstract class to handle the execution of the command requests.
    Acts as the command interface of the Command pattern.
    """

    @abstractmethod
    def execute(self):
        """ Execute method to be overridden by the subclasses """


class AskCommand(Command):
    """ Implements the Command class for an ask request """

    def __init__(self, kwargs, receiver):
        """ Constructor for the AskCommand concrete class."""
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self):
        """ instructions for an ask request """
        self.handler.set_format('xml')
        args = self.handler.combine()
        string = self.receiver.call_main(args)
        return bool('<boolean>true</boolean>' in string)


class ConstructCommand(Command):
    """ Implements the Command class for a construct request """

    def __init__(self, kwargs, receiver):
        """ Constructor for the ConstructCommand concrete class."""
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self):
        """ instructions for a construct request """
        args = self.handler.combine()
        string = self.receiver.call_main(args)
        graph = Graph().parse(data=string)
        return graph


class SelectCommand(Command):
    """ Implements the Command class for a select request """

    def __init__(self, kwargs, receiver):
        """ Constructor for the SelectCommand concrete class."""
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self):
        """ instructions for a select request """
        self.handler.set_format('json')
        args = self.handler.combine()
        string = self.receiver.call_main(args)
        return json.loads(string)


class RunCommand(Command):
    """ Implements the Command class for a run request """

    def __init__(self, kwargs, receiver):
        """ Constructor for the RunCommand concrete class."""
        self.handler = ParameterHandler(kwargs)
        self.receiver = receiver

    def execute(self):
        """ instructions for a run request """
        args = self.handler.combine()
        self.receiver.main(args)
