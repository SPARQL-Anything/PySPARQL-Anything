"""
@author Marco Ratta
@ version 21/01/2023
"""


class Parameters:
    """
    Class to handle the pre-processing of the query parameters.
    """

    def __init__(self):
        """ Constructor for the class Parameters. """

    def makeArgs(self, aDict: dict):
        """
        Helper for the run method. Constructs the appropriate String array
        to pass to the main method from Python **kwargs.
        @param aDict a Python dictionary.
        @return an array of String
        """
        # initialises String[]:
        arguments = []
        # Sets -q and its value as the first two elements. Deletes 'q'.
        if 'q' in aDict:
            arguments.append('-' + 'q')
            arguments.append(aDict['q'])
            aDict.pop('q')
            # Constructs the rest of arguments.
            for key in aDict.keys():
                arguments.append('-' + key)
                arguments.append(aDict[key])
        else:
            print('Invalid argument given. Flag "q" must be passed.')
        # arguments to be passed to the main function.
        return arguments
