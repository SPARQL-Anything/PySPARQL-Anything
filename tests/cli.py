"""
PySPARQL Anything CLI tool test script.
Author: Marco Ratta
Version: 19/12/2023
"""
from argparse import ArgumentParser, Namespace, SUPPRESS
from pysparql_anything.sparql_anything_reflection import SPARQLAnythingReflection
from pysparql_anything.__about__ import __jarMainPath__


def transform_cli_args(args: dict[str, str | list[str]]) -> list[str]:
    # Constructs the list of args to return:
    final_args: list[str] = []
    for k, v in args.items():
        if isinstance(v, list):
            for v_arg in v:
                final_args.extend(['--' + k, v_arg])
        else:
            final_args.extend(['--' + k, v])
    return final_args


def transform_jvm_args(args: str | list[str]) -> str | tuple[str]:
    return tuple(["-" + j_arg for j_arg in args])


def setup_parser(a_parser: ArgumentParser) -> ArgumentParser:
    # Define CLI arguments
    a_parser.add_argument(
        "-q", "--query",
        help="The path to the file storing the query "
        + "to execute or the query itself."
    )
    a_parser.add_argument(
        "-o", "--output",
        help="The path to the output file. [Default: STDOUT]"
    )
    a_parser.add_argument(
        "-f", "--format",
        help="Format of the output file. Supported values: JSON, XML,"
        + " CSV, TEXT, TTL, NT, NQ. [Default:TEXT or TTL]"
    )
    a_parser.add_argument(
        "-l", "--load",
        help="The path to one RDF file or a folder including a set of "
        + "files to be loaded. When present, the data is loaded in memory "
        + " and the query executed against it."
    )
    a_parser.add_argument(
        "-v", "--values", nargs="*",
        help="Values passed as input parameter to a query template.\n"
        + " When by substituting variable names with the values provided.\n"
        + " The argument can be used in two ways:\n "
        + "(1) Providing a single SPARQL ResultSet file. In this case,\n"
        + "the query is executed for each set of bindings in the input "
        + "result set.\n"
        + "Only 1 file is allowed."
        + "(2) Named variable bindings: the argument value must follow"
        + " the syntax:\n"
        + "var_name=var_value. The argument can be passed multiple times and"
        + " the query repeated for each set of values."
    )
    a_parser.add_argument(
        "-j", "--java", nargs="*",
        help="The JVM initialisation options"
    )
    return a_parser


def setup_args(
        args: dict[str, str | list[str]]
        ) -> tuple[str | tuple[str], list[str]]:
    args_jvm = ""
    if "java" in args:
        args_jvm = transform_jvm_args(args["java"])
        args.pop("java")
    args_main = transform_cli_args(args)
    return (args_jvm, args_main)


def main() -> None:
    # Setup a parser object
    parser = setup_parser(
        ArgumentParser(
            prog="sparql-anything",
            description="Welcome to the PySPARQL Anything CLI."
            + " For the optional flags see below.",
            argument_default=SUPPRESS
        )
    )
    # Process the arguments for the Java main class.
    args: Namespace = parser.parse_args()
    java_args = setup_args(vars(args))
    # Run the query
    sa = SPARQLAnythingReflection(java_args[0], __jarMainPath__)
    sa.main(java_args[1])


if __name__ == '__main__':
    main()
