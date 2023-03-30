"""
@author Marco Ratta
@version 09/02/2023
"""


class ParameterHandler:
    """ Class to handle the processing of the query paramters passed
    to the CLI/API methods.
    """

    def __init__(self, kwargs: dict):
        """ Initialiser for the ParameterHandler class.
        Stores the passed parameters and processes them to the form
        required by the SPARQL Anything Main class.
        """
        self.query = self.__query(kwargs)
        self.output = self.__output(kwargs)
        self.explain = self.__explain(kwargs)
        self.load = self.__load(kwargs)
        self.format = self.__format(kwargs)
        self.strategy = self.__strategy(kwargs)
        self.pattern = self.__pattern(kwargs)
        self.values = self.__values(kwargs)

    def combine(self) -> list[str]:
        """ Constructs the appropriate String array to pass to
        the main method from the attributes of this parameter object.
        """
        args = []
        #  Dictionary representation of the state of the object.
        state = dict(filter(pop_empty, vars(self).items())) 
        if state.get('query') != None:
            args.append('-' + 'q')
            args.append(state.get('query'))
            state.pop('query')
        else:
            print('Invalid argument given. Flag "q" must be passed.')
            return args
        if state.get('values') != None:  # Then it is a list.
            for value in state.get('values'):
                args.append('-' + 'v')
                args.append(value)
            state.pop('values')
        for field in state:  # Loops though the remaining flags.
            args.append('-' + field[0:1])
            args.append(state.get(field))
        return args

    def __query(self, kwargs: dict) -> str:
        """ Processes the query parameter. """
        return kwargs.get('q', '')

    def __output(self, kwargs: dict) -> str:
        """ Processes the output parameter. """
        return kwargs.get('o', '')

    def __explain(self, kwargs: dict) -> str:
        """ Processes the explain parameter. """
        return kwargs.get('e', '')

    def __load(self, kwargs: dict) -> str:
        """ Processes the load parameter. """
        return kwargs.get('l', '')

    def __format(self, kwargs: dict) -> str:
        """ Processes the format parameter. """
        return kwargs.get('f', '')

    def __strategy(self, kwargs: dict) -> str:
        """ Processes the strategy parameter. """
        return kwargs.get('s', '')

    def __pattern(self, kwargs: dict) -> str:
        """ Processes the pattern parameter. """
        return kwargs.get('p', '')

    def __values(self, kwargs: dict) -> list[str] | str:
        """ Processes the values parameter. """
        values = kwargs.get('v', '')
        if values != '':
            params = []
            for key, value in values.items():
                params.append(key + '=' + value)
            return params
        return values

    def set_format(self, a_format: str) -> None:
        """ Setter method for the self.format field."""
        self.format = a_format

#  Lambdas
pop_empty = lambda x: x[1] != '' #  Predicate.