"""
This module contains the SparqlAnythingReflection class, which handles the
reflection of the SPARQLAnything class into Python.

@author Marco Ratta
@version 01/07/2023
"""

import jnius_config
from pysparql_anything.config import get_path2jar


class SparqlAnythingReflection:
    """
    The class SparqlAnythingReflection wraps the Java SPARQL Anything Main
    class.

    It makes available its public static void main(String[] args)
    and public static String callMain(String args) methods to Python users.

    This it does by reflecting the SPARQLAnything class in SPARQLAnything.java
    and assigning it to its 'reflection' field.
    """

    def __init__(self, jvm_options: tuple[str]) -> None:
        """
        Initialiser for the class SparqlAnythingReflection.

        Parameters:

        *jvm_options - the options to be passed to the JVM before launch.
        """
        # Sets the JVM classpath to the Sparql Anything installation:
        if jvm_options != tuple():
            for option in jvm_options:
                jnius_config.add_options(option)
        jnius_config.set_classpath(get_path2jar())
        # Starts the JVM and reflects the SPARQLAnything class.
        from jnius import autoclass
        location = 'com.github.sparqlanything.cli.SPARQLAnything'
        self.reflection = autoclass(location)
        # Setting jnius_config.vm_running to False is required in order to
        # assign to each instance of this class its own JVM and SPARQLAnything
        # reflection.
        jnius_config.vm_running = False

    def main(self, args: list[str]) -> None:
        """
        Wrapper for the public static void main(String[] args) method of
        SPARQLAnything.

        Parameters:

        args - args is a Python list[str] that mirrors the String[] args that
            is required by main(String[] args).
        """
        self.reflection.main(args)

    def call_main(self, args: list[str]) -> str:
        """
        Wrapper for the public static String callMain(String args) method of
        SPARQLAnything.

        Parameters:

        args - args is a Python list[str] that mirrors the String[] args that
            is required by callMain(String[] args).
        """
        return self.reflection.callMain(args)
