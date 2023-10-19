'''
This module contains a set of functions whose objective is to change the form 
of theparameters passed to the SparqlAnything methods into the form required by
the Java methods reflected, i.e. main(String[]) and callMain(String[]).

@author Marco Ratta
@version 15/07/2023
'''


def transform_parameters(kwargs: dict) -> list[str]:
    # Takes the dict and returns the sorted parameters
    args = []
    parameters = sort_kwargs(kwargs)
    if parameters.get('query') is not None:
        args.append('-' + 'q')
        args.append(parameters.get('query'))
        parameters.pop('query')
    else:
        print('Invalid argument given. Flag "q" must be passed.')
        return args
    if parameters.get('values') is not None:  # Then it is a list.
        for value in parameters.get('values'):
            args.append('-' + 'v')
            args.append(value)
        parameters.pop('values')
    for flag in parameters:  # Loops though the remaining flags.
        args.append('-' + flag[0:1])
        args.append(parameters.get(flag))
    return args


def sort_kwargs(kwargs: dict) -> dict:
    # takes the dict and sorts it.
    new = dict()
    new['query'] = kwargs.get('q', '')
    new['output'] = kwargs.get('o', '')
    new['explain'] = kwargs.get('e', '')
    new['load'] = kwargs.get('l', '')
    new['format'] = kwargs.get('f', '')
    new['strategy'] = kwargs.get('s', '')
    new['pattern'] = kwargs.get('p', '')
    new['values'] = values(kwargs)
    return dict(filter(lambda x: x[1] != '', new.items()))


def values(kwargs: dict) -> list[str] | str:
    """ Processes the values parameter. """
    values = kwargs.get('v', '')
    if values != '':
        params = []
        for key, value in values.items():
            params.append(key + '=' + value)
        return params
    return values
