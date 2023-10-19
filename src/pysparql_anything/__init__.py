"""
Manages the package's namespace, helps the installation process of the API.

@author Marco Ratta
@version 31/01/2023
"""

import requests
from github.GithubException import RateLimitExceededException
from pysparql_anything import utilities

# Checks if SPARQL Anything is not installed. Installs it if so.
try:
    if not utilities.has_jar():  # SPARQL Anything not installed.
        print('No SPARQL Anything jar has been found'
              + ' in the installation folder.')
        utilities.download_jar()
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
