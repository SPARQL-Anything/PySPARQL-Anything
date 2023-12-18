"""
PySPARQL Anything CLI tool test script.
Author: Marco Ratta
Version: 18/12/2023
"""
from argparse import ArgumentParser, Namespace
# from pysparql_anything.parameter_handler import transform_cli_args
from pysparql_anything.sparql_anything_reflection import SPARQLAnythingReflection
from pysparql_anything.__about__ import __jarMainPath__


def transform_cli_args(args: dict[str, str | None]) -> list[str]:
    # Removes any k, v pair where v = None:
    purged_args = {k: v for k, v in args.items() if v is not None}
    # Constructs the list of args to return:
    final_args: list[str] = []
    for k, v in purged_args.items():
        if isinstance(v, list):
            final_args.extend(['--' + k, v[0], '--' + k, v[1]])
        else:
            final_args.extend(['--' + k, v])
    return final_args


# Create a parser object
parser = ArgumentParser()

# Define the CLI arguments
parser.add_argument('-q', '--query')
parser.add_argument('-o', '--output')
parser.add_argument('-f', '--format')
parser.add_argument('-l', '--load')
parser.add_argument('-v', '--values', action='append')

# Process the arguments for the Java code
args: Namespace = parser.parse_args()
args_dict = vars(args)
java_args = transform_cli_args(args_dict)

# Run the query
reflection = SPARQLAnythingReflection('', __jarMainPath__)
reflection.main(java_args)
