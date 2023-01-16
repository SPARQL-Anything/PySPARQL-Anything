# Configuration script for PySPARQL Anything.
# Aids the installation process.
#
# @author Marco Ratta
# @version v1.0 12/01/2023

import requests
from bs4 import BeautifulSoup
import os

# Checks the jar has been succesfully downloaded in the installation folder.

def checkJAR():
    destination = os.path.join(getPath(), 'sparql.anything.jar')
    return os.path.exists(destination)

# Scrapes the SPARQL Anything latest release page for a version number and
# builds the download link to the jar of the latest release.
# @return The URL to the jar for the latest SPARQL Anything release.

def getURL():
    page = 'https://github.com/SPARQL-Anything/sparql.anything/releases/latest'
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = str(soup.title)
    version = ''
    for token in s.split():
        if token.startswith('v'):
            version = token[1:]
    download = '/download/sparql-anything-{}.jar'.format(version)
    return page + download

# Downloads the jar to the PySPARQL Anything installation folder.

def getJAR():
    print('Downloading the latest SPARQL Anything jar, please wait...')
    r = requests.get(getURL())
    destination = os.path.join(getPath(), 'sparql.anything.jar')
    print('Saving the SPARQL Anything jar, almost there!')
    try:
        with open(destination, 'wb') as f:
           f.write(r.content)
    except:
        print('WARNING!!! SPARQL Anything unsuccesfully installed!!! \n'
              + 'Request Exception occurred.')
    if checkJAR() == True:
        print('SPARQL Anything succesfully installed')

# Returns the path to the PySPARQL Anything installation folder.

def getPath():
    path = os.path.realpath(os.path.dirname(__file__))
    return path


    

