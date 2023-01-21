"""
Configuration and utilities module for PySPARQL Anything.
Aids the installation and maintainment process of the API.
Interacts with the SPARQL Anything GitHub repository.
@author Marco Ratta
@version 21/01/2023
"""


import os
from github import Github
import requests
from tqdm import tqdm


def isJar():
    """
    Checks the jar has been succesfully downloaded in
    the installation folder.
    @return A diagnostic Boolean
    """
    files = os.listdir(getPath())
    for file in files:
        if '.jar' in file:
            return True
    return False


def getUrl():
    """
    Retrieves the download url for latest SPARQL Anything release.
    @return The URL to the jar for the latest SPARQL Anything release
    as a String.
    """
    g = Github()
    uri = 'SPARQL-Anything/sparql.anything'
    release = g.get_repo(uri).get_latest_release()
    assets = release.get_assets()
    jar = ''
    for asset in assets:
        if 'server' not in asset.name:
            jar = asset
    return jar.browser_download_url


def getLatestReleaseTitle():
    """
    Retrieves the latest release version of SPARQL Anything available.
    @return A String containing the latest release version.
    """
    g = Github()
    uri = 'SPARQL-Anything/sparql.anything'
    release = g.get_repo(uri).get_latest_release()
    return release.title


def downloadJar():
    """
    Downloads the latest SPARQL Anything jar to the PySPARQL Anything
    installation folder.
    """
    print('Downloading the latest SPARQL Anything jar, please wait...')
    r = requests.get(getUrl(), stream=True)  # Get request
    length = int(r.headers.get('content-length', 0))
    version = getLatestReleaseTitle()
    path2Jar = os.path.join(getPath(), 'sparql-anything-{}.jar'.format(version))
    try:
        with open(path2Jar, 'wb') as f:
            with tqdm(desc='Downloading SPARQL Anything {}'.format(version),
                      total=length, unit='iB', unit_scale=True,
                      unit_divisor=1024) as pbar:
                for data in r.iter_content(chunk_size=1024):
                    size = f.write(data)
                    pbar.update(size)
        print('The Download was succesful!')
        print('The system is now ready for use!')
    except:
        print('WARNING!!! SPARQL Anything unsuccesfully installed!!! \n'
              + 'Something has gone wrong!!.')


def getPath():
    """
    Function to return the path to the PySPARQL Anything installation folder.
    @return The path String to the PySPARQL Anything installation folder.
    """
    path = os.path.realpath(os.path.dirname(__file__))
    return path


def getPath2Jar():
    """
    Returns the path to the PySPARQL Anything jar currently in use in the
    installation folder.
    @return The path String to the SPARQL Anything jar in use.
    """
    files = os.listdir(getPath())
    path = ''
    for file in files:
        if '.jar' in file:
            path = os.path.join(getPath(), file)
    return path


def check4Update():
    """
    Function to check if a SPARQL Anything update is available to download.
    @return A diagnostic Boolean.
    """
    latest = getLatestReleaseTitle()
    current = ''
    files = os.listdir(getPath())
    for file in files:
        if '.jar' in file:
            current = file[16:22]
    return not current == latest
