"""
Module containing functions aiding the installation and maintainment
process of PySPARQL Anything.
@author Marco Ratta
@version 05/02/2023
"""

import os
from github import Github
from github.GithubException import RateLimitExceededException
import requests
from tqdm import tqdm


def has_jar() -> bool:
    """ Checks the jar has been succesfully downloaded in
    the installation folder.
    """
    files = os.listdir(get_path())
    for file in files:
        if '.jar' in file:
            return True
    return False


def get_url() -> str:
    """ Retrieves the download url for latest SPARQL Anything release.
    @raises RateLimitExceededException
    """
    ghub = Github()
    uri = 'SPARQL-Anything/sparql.anything'
    try:
        release = ghub.get_repo(uri).get_latest_release()
        assets = release.get_assets()
        jar = ''
        for asset in assets:
            if 'server' not in asset.name:
                jar = asset
        return jar.browser_download_url
    except RateLimitExceededException as exc:
        print('WARNING !!! get_url()raised a '
              + f'{type(exc)} exception and passed it on.')
        raise


def get_latest_release_title() -> str:
    """ Retrieves the latest release version of SPARQL Anything available.
    @raises RateLimitExceededException
    """
    ghub = Github()
    uri = 'SPARQL-Anything/sparql.anything'
    try:
        release = ghub.get_repo(uri).get_latest_release()
        return release.title
    except RateLimitExceededException as exc:
        print('WARNING !!! get_latest_release_title()raised a '
              + f'{type(exc)} exception and passed it on.')
        raise


def download_jar() -> None:
    """ Downloads the latest SPARQL Anything jar to the PySPARQL Anything
    installation folder.
    @raises ConnectionError and Timeout
    """
    print('Downloading the latest SPARQL Anything jar, please wait...')
    try:
        version = get_latest_release_title()
        path2jar = os.path.join(get_path(), f'sparql-anything-{version}.jar')
        request = requests.get(get_url(), stream=True, timeout=10.0)
        length = int(request.headers.get('content-length', 0))
        with open(path2jar, 'wb') as jar:
            with tqdm(desc=f'Downloading SPARQL Anything {version}',
                      total=length, unit='iB', unit_scale=True,
                      unit_divisor=1024) as pbar:
                for data in request.iter_content(chunk_size=1024):
                    size = jar.write(data)
                    pbar.update(size)
        print('The Download was successful!')
        print('The system is now ready for use!')
    except requests.ConnectionError as err:
        print('WARNING!!! download_jar() caught '
              + f'a {type(err)} exception and passed it on.')
        raise
    except requests.Timeout as exc:
        print('WARNING!!! download_jar() caught '
              + f'a {type(exc)} exception and passed it on.')
        raise
    except RateLimitExceededException as exc:
        print('WARNING !!! download_jar()raised a '
              + f'{type(exc)} exception and passed it on.')
        raise


def get_path() -> str:
    """
    Function to return the path to the PySPARQL Anything installation folder.
    """
    path = os.path.realpath(os.path.dirname(__file__))
    return path


def get_path2jar() -> str:
    """ Returns the path to the PySPARQL Anything jar currently in use in the
    installation folder.
    """
    files = os.listdir(get_path())
    path = ''
    for file in files:
        if '.jar' in file:
            path = os.path.join(get_path(), file)
    return path


def remove_jar() -> None:
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
