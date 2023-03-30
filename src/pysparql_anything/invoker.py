"""
@author Marco Ratta
@version 05/02/2023
"""

from typing import Any
from pysparql_anything.command import Command


class Invoker:
    """ Invoker class for the implementation of
    the Command pattern.
    """

    def __init__(self):
        """ Initialiser for the class Invoker. """
        self.command: Command

    def set_command(self, command: Command) -> None:
        """ Setter for the command field. """
        self.command = command

    def run_query(self) -> Any:
        """ Invokes the execution of the passed command object. """
        return self.command.execute()
