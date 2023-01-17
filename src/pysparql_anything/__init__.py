# Manages the package's namespace, helps the installation and maintainment
# process of the API.
#
# @author Marco Ratta
# @version 17/01/2023 

# Version variable for build purposes. 'x.y.z' refers to the current release of
# SPARQL Anything, the letter at the end to the independent PySPARQL Anything
# releases.

__version__ = '0.8.1c'

# import statements and namespace configuration
from pysparql_anything.sparql_anything import SparqlAnything
from pysparql_anything import config

# Installation helper. Checks for updates, updates or installs the
# SPARQL Anything jar if it is not already present.

if config.isJar()and config.check4update():
    # An update is available. Prompts the user to confirm the download
    inp = input('An update is available!'
                + ' Would you like to download it? (Yes/No)\n')
    if inp.casefold().__eq__('yes'): 
        from os import remove # Removes the old jar.
        remove(config.getPath2Jar())
        if not config.isJar(): # Removal succesful.
            print('SPARQL Anything succesfully removed')
            config.downloadJar()
            print('The system is now ready for use!')
        else:
            print('SPARQL Anything unsuccesfully removed! \n'
                  +'Cannot execute the update process!')
    else: # User input = 'No'.
        print('The system is ready for use!')   
elif config.isJar() and not config.check4update(): # Everything is up to date.
    pass
else: # SPARQL Anything not installed.
    print('No SPARQL Anything jar has been found in the installation folder.')
    config.downloadJar()
    print('The system is now ready for use!')





