"""
@author Marco Ratta
@ version 24/01/2023
"""

import json
from abc import ABC, abstractmethod
from rdflib import Graph
from pysparql_anything.engine import Engine


class Command(ABC):
    """
    Abstract class to handle the pre-processing of the query parameters and
    the execution of the command requests.
    Acts as the command class of a Command pattern.
    """

    receiver = Engine() # Composition with SPARQL Anything.

    def __init__(self, kwargs: dict):
        """ Constructor for the class Command.
        Models a query command to be sent to the SA Engine.
        """
        self.query = self.__query(kwargs)
        self.output = self.__output(kwargs)
        self.explain = self.__explain(kwargs)
        self.load = self.__load(kwargs)
        self.format = self.__format(kwargs)
        self.strategy = self.__strategy(kwargs)
        self.pattern = self.__pattern(kwargs)
        self.values = self.__values(kwargs)

    @abstractmethod
    def execute(self):
        """ Execute method to be overridden by the subclasses """

    def _combine(self):
        """
        Constructs the appropriate String array to pass to
        the main method from the attributes of this parameter object.
        @return an array of type String
        """
        args = []
        state = vars(self)
        if state.get('query') != '':
            args.append('-' + 'q')
            args.append(state.get('query'))
            state.pop('query')
        else:
            print('Invalid argument given. Flag "q" must be passed.')
            return args
        if state.get('values') != '':  # Then it is a list.
            for value in state.get('values'):
                args.append('-' + 'v')
                args.append(value)
            state.pop('values')
        for field in state:  # Loops though the remaining flags.
            if state.get(field) != '':
                args.append('-' + field[0:1])
                args.append(state.get(field))
        return args

    def __query(self, kwargs):
        """ Processes the query parameter. """
        return kwargs.get('q', '')

    def __output(self, kwargs: dict):
        """ Processes the output parameter. """
        return kwargs.get('o', '')

    def __explain(self, kwargs: dict):
        """ Processes the explain parameter. """
        return kwargs.get('e', '')

    def __load(self, kwargs: dict):
        """ Processes the load parameter. """
        return kwargs.get('l', '')

    def __format(self, kwargs: dict):
        """ Processes the format parameter. """
        return kwargs.get('f', '')

    def __strategy(self, kwargs: dict):
        """ Processes the strategy parameter. """
        return kwargs.get('s', '')

    def __pattern(self, kwargs: dict):
        """ Processes the pattern parameter. """
        return kwargs.get('p', '')

    def __values(self, kwargs: dict):
        """ Processes the values parameter. """
        values = kwargs.get('v', '')
        if values != '':
            params = []
            for key, value in values.items():
                params.append(key + '=' + value)
            return params
        return values


class AskCommand(Command):
    """ Implements the Command class for an ask request """

    def __init__(self, kwargs):
        """ Constructor for the AskCommand concrete class."""
        super().__init__(kwargs)
        self.format = 'xml'

    def execute(self):
        """ instructions for an ask request """
        args = super()._combine()
        string = Command.receiver.call_main(args)
        return bool('<boolean>true</boolean>' in string)


class ConstructCommand(Command):
    """ Implements the Command class for a construct request """

    def __init__(self, kwargs):
        """ Constructor for the ConstructCommand concrete class."""
        super().__init__(kwargs)

    def execute(self):
        """ instructions for a construct request """
        args = super()._combine()
        string = Command.receiver.call_main(args)
        graph = Graph().parse(data=string)
        return graph


class SelectCommand(Command):
    """ Implements the Command class for a select request """

    def __init__(self, kwargs):
        """ Constructor for the SelectCommand concrete class."""
        super().__init__(kwargs)
        self.format = 'json'

    def execute(self):
        """ instructions for a select request """
        args = super()._combine()
        string = Command.receiver.call_main(args)
        return json.loads(string)


class RunCommand(Command):
    """ Implements the Command class for a run request """

    def __init__(self, kwargs):
        """ Constructor for the RunCommand concrete class."""
        super().__init__(kwargs)

    def execute(self):
        """ instructions for a run request """
        args = super()._combine()
        Command.receiver.main(args)
