"""
This module contains the functions that change the form of the arguments
given to the SparqlAnything methods into the form required by
the reflected Java methods, i.e. main(String[]) and callMain(String[]).

Author: Marco Ratta
Date: 10/10/2024
"""
import argparse
from collections.abc import Sequence


# Helper functions for the API methods
def transform_args(kwargs: dict[str, str | dict[str, str]]) -> list[str]:
    """
    This method transforms the request's arguments, passed as a dictionary,
    into the list[str] required by the Java methods.\n
    Args:\n
        kwargs - a dictionary containing the request's arguments.\n
    Returns:\n
        A list of str containing the query's arguments in the style accepted
        by a Java main method.\n
    Raises:\n
        ValueError if no query argument has been passed.
    """
    args = []
    for flag in kwargs:
        #if flag in ['v', 'c', 'values', 'configuration']:
        flag_image = kwargs[flag]
        if isinstance(flag_image, dict):
            values_list = [k + '=' + v for k, v in flag_image.items()]
            for value in values_list:
                args += [
                    '-' + flag if len(flag) == 1 else '--' + flag, value
                ]
        else:
            args += [
                '-' + flag if len(flag) == 1 else '--' + flag, flag_image
            ]
    return args


# Helper functions for the CLI
def transform_cli_flags(args: dict[str, str | list[str]]) -> list[str]:
    """
    Transforms the passed optional arguments for the CLI into the form
    required by the SPARQLAnythingReflection main method.\n
    Args:\n
        args: A dict containing the parsed CLI flags arguments.\n
    Returns:\n
        A list[str] of arguments for the Java main method.
    Raises:\n
        ValueError if no query argument has been passed.
    """
    if "query" not in args:
        raise ValueError(
            "Invalid arguments given. A query must be passed.\n"
            + "Type sparql-anything -h in your terminal for usage help."
        )
    final_args: list[str] = []
    for k, v in args.items():
        if isinstance(v, list):
            for v_arg in v:
                final_args.extend(['--' + k, v_arg])
        else:
            final_args.extend(['--' + k, v])
    return final_args


def transform_jvm_flags(args: list[str]) -> list[str]:
    """
    Transforms the passed optional arguments for the JVM into the form
    required by the SPARQLAnythingReflection constructor.\n
    Args:\n
        args: The string or list[str] of JVM arguments.\n
    Returns:\n
        A string or tuple[str] containing the JVM arguments.
    """
    return ["-" + j_arg for j_arg in args]


def transform_cli_args(
        args: argparse.Namespace
        ) -> tuple[list[str], list[str]]:
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
    args_jvm = list()
    if hasattr(args, "java"):
        args_jvm = transform_jvm_flags(args.java)
        args_dict.pop("java")
    args_main = [
        '--output-pattern' if x == '--output_pattern' else x
        for x in transform_cli_flags(args_dict)
    ]
    return (args_jvm, args_main)
