"""
@author Marco Ratta
@version 02/02/2023
"""


class ParameterHandler:
    """
    Class to handle the processing of the query paramters passed
    to the CLI/API methods.
    """

    def __init__(self, kwargs: dict):
        """ Constructor for the ParameterHandler class.
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

    def combine(self):
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
            if (state.get(field) != '') and (field != 'receiver'):
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

    def set_format(self, a_format: str):
        """ Setter method for the self.format field."""
        self.format = a_format
