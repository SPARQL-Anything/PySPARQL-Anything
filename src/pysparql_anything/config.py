# Configuration and utilities module for PySPARQL Anything.
# Aids the installation and maintainment process of the API.
# Interacts with the SPARQL Anything GitHub repository.
#
# @author Marco Ratta
# @version v1.1 16/01/2023

from github import Github
import requests
import os
from tqdm import tqdm

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

# Retrieves the latest release version of SPARQL Anything available.
# @return A String containing the latest release version.

def getLatestReleaseTitle():
    g = Github()
    release = g.get_repo('SPARQL-Anything/sparql.anything').get_latest_release()
    return release.title        

# Downloads the latest SPARQL Anything jar to the PySPARQL Anything
# installation folder.

def downloadJar():
    print('Downloading the latest SPARQL Anything jar, please wait...')
    r = requests.get(getUrl(), stream = True) # Get request
    length = int(r.headers.get('content-length', 0))
    version = getLatestReleaseTitle()
    path2Jar = os.path.join(getPath(), 'sparql-anything-{}.jar'.format(version))
    try:
        with open(path2Jar, 'wb') as f:
            with tqdm(desc = 'Downloading SPARQL Anything {}'.format(version),
                      total = length, unit = 'iB', unit_scale = True,
                      unit_divisor = 1024) as pbar:
                for data in r.iter_content(chunk_size = 1024):
                    size = f.write(data)
                    pbar.update(size)
        print('The Download was succesful!')
    except:
        print('WARNING!!! SPARQL Anything unsuccesfully installed!!! \n'
              + 'Something has gone wrong!!.')

# Function to return the path to the PySPARQL Anything installation folder.
# @return The path String to the PySPARQL Anything installation folder.

def getPath():
    path = os.path.realpath(os.path.dirname(__file__))
    return path

# Returns the path to the PySPARQL Anything jar currently in use in the
# installation folder.
# @return The path String to the SPARQL Anything jar in use.

def getPath2Jar():
    files = os.listdir(getPath())
    path =''
    for file in files:
        if 'sparql-anything-v' and '.jar' in file:
            path = os.path.join(getPath(), file)
    return path

# Function to check if a SPARQL Anything update is available to download.
# @return A diagnostic Boolean.

def check4update():
    latest = getLatestReleaseTitle()
    current = ''
    files = os.listdir(getPath())
    for file in files:
        if 'sparql-anything-v' and '.jar' in file:
            current = file[16:22]
    if current.__eq__(latest): # Everything is up to date.
        return False
    else:
        return True

    

