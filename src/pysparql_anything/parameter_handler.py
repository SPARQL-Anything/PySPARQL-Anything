'''
This module contains the functions that change the form of the arguments
given to the SparqlAnything methods into the form required by
the reflected Java methods, i.e. main(String[]) and callMain(String[]).

@author Marco Ratta
@version 26/10/2023
'''


def transform_parameters(kwargs: dict) -> list[str]:
    '''
    This method is the interface of this module. It transforms the request's
    arguments, passed as a dictionary, into the list[str] required by the Java
    methods.\n
    Arguments:\n
    kwargs - a dictionary containing the request's arguments.
    '''
    args = []
    # Transforms the 'q' keyword arg:
    q_value: str | None = kwargs.get('q')
    if q_value is not None:
        args += ['-q', q_value]
        kwargs.pop('q')
    else:
        print('Invalid argument given. Flag "q" must be passed.')
        return args
    # Transforms the 'v' keyword arg:
    v: dict[str, str] | None = kwargs.get('v')
    if v is not None:
        v_list = [k + '=' + v for k, v in v.items()]
        for v_value in v_list:
            args += ['-v', v_value]
        kwargs.pop('v')
    # Transforms the remaining keyword args:
    for flag in kwargs:  # flag: str | None.
        args += ['-' + flag[0:1], kwargs.get(flag)]
    return args
