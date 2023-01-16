# Manages the package's namespace, helps the installation and maintainment
# process of the API.
#
# @author Marco Ratta
# @version 16/01/2023 v1.0 

# Version variable for build purposes. 'x.y.z' refers to the current release of
# SPARQL Anything, the letter at the end to the independent PySPARQL Anything
# releases.

__version__ = "v0.8.1a"

# import statements and namespace configuration
from pysparql_anything.sparql_anything import SparqlAnything
from pysparql_anything import config

# Installation helper. Checks and installs the SPARQL Anything jar if not
# already present.

if config.checkJAR():
    pass
else:
    config.getJAR()
    
