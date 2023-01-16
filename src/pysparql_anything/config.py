# Configuration and utilities module for PySPARQL Anything.
# Aids the installation and maintainment process of the API.
# Interacts with the SPARQL Anything GitHub repository.
#
# @author Marco Ratta
# @version v1.1 16/01/2023

from github import Github
import requests
import os

# Checks the jar has been succesfully downloaded in the installation folder.
# @return A diagnostic Boolean

def isJar():
    files = os.listdir(getPath())
    for file in files:
        if 'sparql-anything-v' and '.jar' in file:
            return True
    return False

# Retrieves the download url for latest SPARQL Anything release.
# @return The URL to the jar for the latest SPARQL Anything release as a String.

def getUrl():
    g = Github()
    release = g.get_repo('SPARQL-Anything/sparql.anything').get_latest_release()
    assets = release.get_assets()
    jar = ''
    for asset in assets:
        if 'server' not in asset.name:
            jar = asset
    return jar.browser_download_url

def getLatestReleaseTitle():
    g = Github()
    release = g.get_repo('SPARQL-Anything/sparql.anything').get_latest_release()
    return release.title        

# Downloads the latest SPARQL Anything jar to the PySPARQL Anything
# installation folder.

def getJar():
    print('Downloading the latest SPARQL Anything jar, please wait...')
    r = requests.get(getUrl())
    version = getLatestReleaseTitle()
    path2Jar = os.path.join(getPath(), 'sparql-anything-{}.jar'.format(version))
    print('Saving the SPARQL Anything jar, almost there!')
    try:
        with open(path2Jar, 'wb') as f:
           f.write(r.content)
    except:
        print('WARNING!!! SPARQL Anything unsuccesfully installed!!! \n'
              + 'Request Exception occurred.')
    if isJar() == True:
        print('SPARQL Anything succesfully installed')

# Returns the path to the PySPARQL Anything installation folder.

def getPath():
    path = os.path.realpath(os.path.dirname(__file__))
    return path

# Returns the path to the PySPARQL Anything jar currently in use in the
# installation folder.

def getPath2Jar():
    files = os.listdir(getPath())
    path =''
    for file in files:
        if 'sparql-anything-v' and '.jar' in file:
            path = os.path.join(getPath(), file)
    return path


    

