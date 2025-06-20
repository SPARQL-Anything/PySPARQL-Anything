"""
This module contains the SPARQLAnythingReflection class, which handles the
reflection of the SPARQLAnything class into Python and makes its public static
void main(String[] args) and public static String callMain(String args) methods
to Python users.

Author: Marco Ratta
Date: 18/12/2023
"""

from collections.abc import Sequence
from dataclasses import dataclass
import jnius_config
from pysparql_anything.utilities import get_path2jar
from pysparql_anything.__about__ import __jarMainPath__


@dataclass
class SPARQLAnythingQueryOutput:
    err: str
    out: str


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
        self, jvm_options: Sequence[str]
    ) -> None:
        try:
            # Sets the JVM classpath to the Sparql Anything installation:
            if len(jvm_options) > 0:
                for option in jvm_options:
                    jnius_config.add_options(option)
            jnius_config.set_classpath(get_path2jar())
            # Starts the JVM and reflects the required Java classes:
            from jnius import autoclass
            # Create necessary JAVA Class objects
            self.BAOS = autoclass("java.io.ByteArrayOutputStream")
            self.PrintStream = autoclass("java.io.PrintStream")
            self.System = autoclass("java.lang.System")
            # Redirect Java STDERR
            self.err_bs = self.BAOS()
            self.err_ps = self.PrintStream(self.err_bs, False)
            self.System.setErr(self.err_ps)
            # Create the SPARQLAnything class object
            self.reflection = autoclass(__jarMainPath__)
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

    def call_main(self, args: list[str]) -> SPARQLAnythingQueryOutput:
        """
        Wrapper for the public static String callMain(String args) method of
        SPARQLAnything.\n
        Args:\n
            args: A Python list[str] that mirrors the String[] args that
                is required by callMain(String[] args).\n
        Returns:\n
            A string containing the query output.
        """
        # Capture STDOUT locally
        baos = self.BAOS()
        ps = self.PrintStream(baos, False)
        old_ps = self.System.out
        self.System.setOut(ps)
        # Call Sparql Anything main method
        self.reflection.main(args)
        # Put things back
        self.System.out.flush()
        self.System.setOut(old_ps)
        # Convert streams to strings
        sa_output = baos.toString()
        err_output = self.err_bs.toString().lstrip()
        # Reset the error ByteArrayOutputStream
        self.err_bs.reset()
        return SPARQLAnythingQueryOutput(
            err=err_output, out=sa_output
        )
