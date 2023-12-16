"""
Manages the package's namespace, helps the installation process of the API.

@author Marco Ratta
@version 16/12/2023
"""

import requests
from github import Github
from github.GithubException import RateLimitExceededException
from pysparql_anything import utilities
from pysparql_anything.__about__ import __SparqlAnything__, __uri__, __version__

# Checks if SPARQL Anything is not installed. Installs it if so.
try:
    if not utilities.has_jar():  # SPARQL Anything not installed.
        print(f'Welcome to PySPARQL Anything {__version__}, the SPARQL '
              + 'Anything Python library.')
        print('No SPARQL Anything jar has been found'
              + ' in the installation folder.')
        utilities.download_sparql_anything(
            Github(), __uri__, __SparqlAnything__
        )
except requests.ConnectionError as err:
    print(f' A {type(err)} exception has been raised. \n'
          + 'Installation unsuccessful!!!')
    raise
except requests.Timeout as exc:
    print(f' A {type(exc)} exception has been raised. \n'
          + 'Installation unsuccessful!!!')
    raise
except RateLimitExceededException as exc:
    print(f' A {type(exc)} exception has been raised. \n'
          + 'Installation unsuccessful!!!')
    raise
# Launches the JVM
from pysparql_anything.sparql_anything import SparqlAnything
