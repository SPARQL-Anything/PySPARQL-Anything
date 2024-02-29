"""
This module contains the functions that change the form of the arguments
given to the SparqlAnything methods into the form required by
the reflected Java methods, i.e. main(String[]) and callMain(String[]).

Author: Marco Ratta
Date: 29/02/2024
"""
import argparse


# Helper functions for the API methods
def transform_args(kwargs: dict) -> list[str]:
    """
    This method transforms the request's arguments, passed as a dictionary,
    into the list[str] required by the Java methods.\n
    Args:\n
        kwargs - a dictionary containing the request's arguments.\n
    Returns:\n
        A list of str containing the query's arguments in the style accepted
        by a Java main method.
    """
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


# Helper functions for the CLI
def transform_cli_flags(args: dict[str, str | list[str]]) -> list[str]:
    """
    Transforms the passed optional arguments for the CLI into the form
    required by the SPARQLAnythingReflection main method.\n
    Args:\n
        args: A dict conataining the parsed CLI flags arguments.\n
    Returns:\n
        A list[str] of arguments for the Java main method.
    """
    final_args: list[str] = []
    for k, v in args.items():
        if isinstance(v, list):
            for v_arg in v:
                final_args.extend(['--' + k, v_arg])
        else:
            final_args.extend(['--' + k, v])
    return final_args


def transform_jvm_flags(args: str | list[str]) -> str | tuple[str]:
    """
    Transforms the passed optional arguments for the JVM into the form
    required by the SPARQLAnythingReflection constructor.\n
    Args:\n
        args: The string or list[str] of JVM arguments.\n
    Returns:\n
        A string or tuple[str] containing the JVM arguments.
    """
    return tuple(["-" + j_arg for j_arg in args])


def transform_cli_args(
        args: argparse.Namespace
        ) -> tuple[str | tuple[str], list[str]]:
    """
    Method to transform the CLI optional arguments from an argparse.Namespace
    to the forms required by the SPARQLAnythingReflection method.\n
    Args:\n
        args: A Namespace object containing the parsed CLI arguments.\n
    Returns: \n
        A tuple containing all the arguments required by the constructor and
        main method of SPARQLAnythingReflection.
    """
    args_dict = vars(args)
    args_jvm = ""
    if "java" in args_dict:
        args_jvm = transform_jvm_flags(args_dict["java"])
        args_dict.pop("java")
    args_main = transform_cli_flags(args_dict)
    return (args_jvm, args_main)
