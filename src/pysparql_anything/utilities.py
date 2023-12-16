"""
Configuration and utilities module for PySPARQL Anything.
Aids the installation and maintainment process of the API.
Interacts with the SPARQL Anything GitHub repository.
@author Marco Ratta
@version 16/12/2023
"""

import os
from github import Github
from github.GithubException import RateLimitExceededException
import requests
from tqdm import tqdm


def has_jar():
    """
    Checks the jar has been succesfully downloaded in
    the installation folder.
    @return A diagnostic Boolean
    """
    files = os.listdir(get_module_path())
    for file in files:
        if '.jar' in file:
            return True
    return False


def get_release_uri(ghub: Github, uri: str, version: str) -> str:
    """
    Retrieves the download url for latest SPARQL Anything release.\n
    Args:\n
    ghub - A pyGithub Main object. \n
    uri - the Sparql Anything repo uri. \n
    version - the Sparql Anything version to be downloaded. \n
    Returns:\n
    The URL to the jar for the latest SPARQL Anything release
    as a String.\n
    Raises:\n
    RateLimitExceededException: github.GithubException
    """
    try:
        release = ghub.get_repo(uri).get_release(version)
        assets = release.get_assets()
        jar = ''
        for asset in assets:
            if 'server' not in asset.name:
                jar = asset
        return jar.browser_download_url
    except RateLimitExceededException as exc:
        print('WARNING !!! get_release_url() raised a '
              + f'{type(exc)} exception and passed it on.')
        raise


def download_sparql_anything(ghub: Github, uri: str, version: str) -> None:
    """
    Downloads the passed version of the SPARQL Anything jar to the PySPARQL
    Anything installation folder.\n
    Args:\n
    ghub - A pyGithub Main object. \n
    uri - the Sparql Anything repo uri. \n
    version - the Sparql Anything version to be downloaded. \n
    Raises: \n
    ConnectionError and Timeout.
    """
    try:
        print(f'Downloading SPARQL Anything {version}')
        path2jar = os.path.join(
            get_module_path(), f'sparql-anything-{version}.jar'
        )
        dl_link = get_release_uri(ghub, uri, version)
        request = requests.get(dl_link, stream=True, timeout=10.0)
        length = int(request.headers.get('content-length', 0))
        with open(path2jar, 'wb') as jar:
            with tqdm(colour='green', total=length, unit='iB', unit_scale=True,
                      unit_divisor=1024) as pbar:
                for data in request.iter_content(chunk_size=1024):
                    size = jar.write(data)
                    pbar.update(size)
        print('The Download was successful!')
        print('The system is now ready for use!')
    except requests.ConnectionError as err:
        print('WARNING!!! download_sparql_anything() caught '
              + f'a {type(err)} exception and passed it on.')
        raise
    except requests.Timeout as exc:
        print('WARNING!!! download_sparql_anything() caught '
              + f'a {type(exc)} exception and passed it on.')
        raise
    except RateLimitExceededException as exc:
        print('WARNING !!! download_sparql_anything()raised a '
              + f'{type(exc)} exception and passed it on.')
        raise


def get_module_path():
    """
    Function to return the path to the PySPARQL Anything installation folder.
    @return The path String to the PySPARQL Anything installation folder.
    """
    path = os.path.realpath(os.path.dirname(__file__))
    return path


def get_path2jar():
    """
    Returns the path to the PySPARQL Anything jar currently in use in the
    installation folder.
    @return The path String to the SPARQL Anything jar in use.
    """
    files = os.listdir(get_module_path())
    path = ''
    for file in files:
        if '.jar' in file:
            path = os.path.join(get_module_path(), file)
    return path


def remove_sparql_anything():
    """ Removes the SPARQL Anything jar from the installation folder
    @raises FileNotFoundError
    """
    try:
        os.remove(get_path2jar())
        print("SPARQL Anything sucessfully removed")
    except FileNotFoundError as err:
        print('WARNING !!! download_jar()raised a '
              + f'{type(err)} exception and re-raised it.')
        raise
