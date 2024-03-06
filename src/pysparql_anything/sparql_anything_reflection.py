"""
This module contains the SPARQLAnythingReflection class, which handles the
reflection of the SPARQLAnything class into Python and makes its public static
void main(String[] args) and public static String callMain(String args) methods
to Python users.

Author: Marco Ratta
Date: 18/12/2023
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
    and assigning it to the 'reflection' field of its instance.\n
    Args:\n
        *jvm_options: The options to be passed to the JVM before launch.\n
        jar_main_path: the class path to the SPARQL Anything main class
            in the executable jar.\n
            This is set as default and should not be altered here.\n
    Raises:\n
        ValueError: If more than one JVM is tried to be spawned within
            the same process.\n
        Exception: If the JVM optional arguments are invalid or there is a
            problem with the JVM installation.
    """
    def __init__(
            self, jvm_options: tuple[str], jar_main_path: str = __jarMainPath__
            ) -> None:
        try:
            # Sets the JVM classpath to the Sparql Anything installation:
            if jvm_options != tuple():
                for option in jvm_options:
                    jnius_config.add_options(option)
            jnius_config.set_classpath(get_path2jar())
            # Starts the JVM and reflects the SPARQLAnything class:
            from jnius import autoclass
            self.reflection = autoclass(jar_main_path)
        except ValueError:
            raise
        except Exception:
            print()
            print(
                "".join([
                    "A pyjnius.autoclass exception has been raised.\n",
                    "Either the JVM parameters passed have not been ", 
                    "recognised as valid or there may be an issue with the ",
                    "installation of the JVM."
                ])
            )
            print()
            raise

    def main(self, args: list[str]) -> None:
        """
        Wrapper for the public static void main(String[] args) method of
        SPARQLAnything.\n
        Args:\n
            args: A Python list[str] that mirrors the String[] args that
                is required by main(String[] args).
        """
        self.reflection.main(args)

    def call_main(self, args: list[str]) -> str:
        """
        Wrapper for the public static String callMain(String args) method of
        SPARQLAnything.\n
        Args:\n
            args: A Python list[str] that mirrors the String[] args that
                is required by callMain(String[] args).\n
        Returns:\n
            A string containing the query output.
        """
        return self.reflection.callMain(args)
