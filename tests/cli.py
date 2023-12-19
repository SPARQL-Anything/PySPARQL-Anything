"""
PySPARQL Anything CLI tool test script.
Author: Marco Ratta
Version: 19/12/2023
"""
from argparse import ArgumentParser, Namespace
from pysparql_anything.sparql_anything_reflection import SPARQLAnythingReflection
from pysparql_anything.__about__ import __jarMainPath__


def transform_cli_args(args: dict[str, str | None | list[str]]) -> list[str]:
    # Removes any k, v pair where v = None:
    purged_args = {k: v for k, v in args.items() if v is not None}
    # Constructs the list of args to return:
    final_args: list[str] = []
    for k, v in purged_args.items():
        if isinstance(v, list):
            for v_arg in v:
                final_args.extend(['--' + k, v_arg])
        else:
            final_args.extend(['--' + k, v])
    return final_args


def transform_jvm_args(args: None | str | list[str]) -> str | tuple[str]:
    args_jvm: tuple[str] = ''
    if args is not None:
        args_jvm = tuple(
            ['-' + j_arg for j_arg in args]
        )
    return args_jvm


def setup_parser(a_parser: ArgumentParser) -> ArgumentParser:
    # Define CLI arguments
    a_parser.add_argument('-q', '--query')
    a_parser.add_argument('-o', '--output')
    a_parser.add_argument('-f', '--format')
    a_parser.add_argument('-l', '--load')
    a_parser.add_argument('-v', '--values', action='append')
    a_parser.add_argument('-j', '--java', action='append')
    return a_parser


def setup_args(
        args: dict[str, str | None | list[str]]
        ) -> tuple[str | tuple[str], list[str]]:
    args_jvm = transform_jvm_args(args['java'])
    args.pop('java')
    args_main = transform_cli_args(args)
    return (args_jvm, args_main)


def main() -> None:
    # Setup a parser object
    parser = setup_parser(ArgumentParser())
    # Process the arguments for the Java code
    args: Namespace = parser.parse_args()
    java_args = setup_args(vars(args))
    # Run the query
    reflection = SPARQLAnythingReflection(java_args[0], __jarMainPath__)
    reflection.main(java_args[1])


if __name__ == '__main__':
    main()
