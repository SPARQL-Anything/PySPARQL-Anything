"""
This module contains the SPARQLAnythingReflection class, which handles the
reflection of the SPARQLAnything class into Python and makes its public static
void main(String[] args) and public static String callMain(String args) methods
to Python users.

@author Marco Ratta
@version 18/12/2023
"""

import jnius_config
from pysparql_anything.utilities import get_path2jar
from pysparql_anything.__about__ import __jarMainPath__


class SPARQLAnythingReflection:
    """
    The class SPARQLAnythingReflection wraps the Java SPARQL Anything Main
    class.\n
    It therefore makes available its public static void main(String[] args)
    and public static String callMain(String args) methods to Python users.\n
    This it does by reflecting the SPARQLAnything class in SPARQLAnything.java
    and assigning it to the 'reflection' field of its instance.
    """

    def __init__(
            self, jvm_options: tuple[str], jar_main_path: str = __jarMainPath__
            ) -> None:
        """
        Initialiser for the class SPARQLAnythingReflection.\n
        Arguments:\n
        jvm_options - the options to be passed to the JVM before launch.
        """
        try:
            # Sets the JVM classpath to the Sparql Anything installation:
            if jvm_options != tuple():
                for option in jvm_options:
                    jnius_config.add_options(option)
            jnius_config.set_classpath(get_path2jar())
            # Starts the JVM and reflects the SPARQLAnything class:
            from jnius import autoclass
            self.reflection = autoclass(jar_main_path)
        except ValueError as err:
            print('ValueError:', err)
            raise
        except Exception as exc:
            print('Exception:', exc)
            raise

    def main(self, args: list[str]) -> None:
        """
        Wrapper for the public static void main(String[] args) method of
        SPARQLAnything.\n
        Arguments:\n
        args - args is a Python list[str] that mirrors the String[] args that
            is required by main(String[] args).
        """
        self.reflection.main(args)

    def call_main(self, args: list[str]) -> str:
        """
        Wrapper for the public static String callMain(String args) method of
        SPARQLAnything.\n
        Arguments:\n
        args - args is a Python list[str] that mirrors the String[] args that
            is required by callMain(String[] args).
        """
        return self.reflection.callMain(args)
