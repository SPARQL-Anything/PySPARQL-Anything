"""
This module contains the CLI for the SPARQL Anything tool.

Author: Marco ratta
Date: 11/09/2024
"""

from argparse import ArgumentParser, SUPPRESS
from pysparql_anything.args_handlers import transform_cli_args
from pysparql_anything.sparql_anything_reflection import SPARQLAnythingReflection
from pysparql_anything.__about__ import __jarMainPath__


def setup_parser(a_parser: ArgumentParser) -> ArgumentParser:
    """
    Adds the required flags and argument information to the passed
    ArgumentParser object.\n
    Args:\n
        a_parser: an argparse.ArgumentParser object.\n
    Returns:\n
        The same ArgumentParser object with its arguments setup.
    """
    a_parser.add_argument(
        "-q", "--query",
        help="""
        The path to the file storing the query to execute or the query itself.
        """
    )
    a_parser.add_argument(
        "-j", "--java", nargs="*",
        help="OPTIONAL - The JVM initialisation options."
    )
    a_parser.add_argument(
        "-o", "--output",
        help="OPTIONAL - The path to the output file. [Default: STDOUT]"
    )
    a_parser.add_argument(
        "-p", "--output-pattern",
        help="""
        OPTIONAL - Output filename pattern, e.g. 'my-file-?friendName.json'.
        Variables should start with '?' and refer to bindings from the input
        file. This option can only be used in combination with 'values' and is
        ignored otherwise. This option overrides 'output'.
        """
    )
    a_parser.add_argument(
        "-f", "--format",
        help="""
        OPTIONAL - Format of the output file. Supported values: JSON, XML, CSV,
        TEXT, TTL, NT, NQ. [Default:TEXT or TTL]
        """
    )
    a_parser.add_argument(
        "-l", "--load",
        help="""
        OPTIONAL - The path to one RDF file or a folder including a set of
        files to be loaded. When present, the data is loaded in memory
        and the query executed against it."""
    )
    a_parser.add_argument(
        "-v", "--values", nargs="*",
        help="""
        OPTIONAL - Values passed as input parameter to a query template.
        When present, the query is pre-processed by substituting variable
        names with the values provided.
        The argument can be used in two ways:
        (1) Providing a single SPARQL ResultSet file. In this case,
        the query is executed for each set of bindings in the input result set.
        Only 1 file is allowed.
        (2) Named variable bindings:
        the argument value must follow the syntax: var_name=var_value.
        The argument can be passed multiple times and the query repeated
        for each set of values."""
    )
    a_parser.add_argument(
        "-c", "--configuration", nargs="*",
        help="""
        OPTIONAL - Configuration to be
        passed to the SPARQL Anything
        engine (this is equivalent to
        define them in the SERVICE IRI).
        The argument can be passed multiple
        times (one for each option to be
        set). Options passed in this way
        can be overwritten in the SERVICE
        IRI or in the Basic Graph Pattern.
        """
    )
    a_parser.add_argument(
        "-e", "--explain", help="OPTIONAL - Explain query execution"
    )
    return a_parser


def main() -> None:
    # Setup a parser object
    parser = ArgumentParser(
            prog="sparql-anything",
            description="""Welcome to the PySPARQL Anything CLI.
            For the optional flags see below.""",
            argument_default=SUPPRESS
        )
    parser = setup_parser(parser)
    # Process the arguments for the Java main class.
    args = parser.parse_args()
    java_args = transform_cli_args(args)
    # Run the query
    sa = SPARQLAnythingReflection(java_args[0], __jarMainPath__)
    sa.main(java_args[1])
