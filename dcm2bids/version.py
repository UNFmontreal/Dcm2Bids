# -*- coding: utf-8 -*-


#dcm2bids version
__version__ = "2.1.4"


import logging
import shlex
import socket

from distutils.version import LooseVersion
from subprocess import check_output

try:
    from shutil import which
except:
    #python2 compatibility
    from distutils.spawn import find_executable as which


logger = logging.getLogger(__name__)


def internet(host="8.8.8.8", port=53, timeout=3):
    """ Check if user has internet

    Args:
        host (string): 8.8.8.8 (google-public-dns-a.google.com)
        port (int): OpenPort 53/tcp
                    Service: domain (DNS/TCP)
        timeout (int): default=3

    Returns:
        boolean

    Source: https://stackoverflow.com/a/33117579
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(
                socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True

    except:
        return False


def is_tool(name):
    """ Check if a program is in PATH

    Args:
        name (string): program name
    Returns:
        boolean
    """
    return which(name) is not None


def check_github_latest(githubRepo):
    """ Check the latest version of a github repository

    Args:
        githubRepo (string): a github repository ("username/repository")

    Returns:
        A string of the version
    """
    url = "https://github.com/{}/releases/latest".format(githubRepo)
    try:
        output = check_output(shlex.split("curl --silent " + url))
    except:
        logger.debug(
                "Checking latest version of {} was not possible".format(
                    githubRepo), exc_info=True)
        return

    #The output should have this format
    #<html><body>You are being <a href="https://github.com/{gitRepo}/releases/tag/{version}">redirected</a>.</body></html>
    try:
        return output.decode().split(
                "{}/releases/tag/".format(githubRepo))[1].split('"')[0]
    except:
        logger.debug(
                "Checking latest version of {} was not possible".format(
                    githubRepo), exc_info=True)
        return


def check_latest(name="dcm2bids"):
    """ Check if a new version of a software exists and print some details
    Implemented for dcm2bids, dcm2niix

    Args:
        name (string): name of the software

    Returns:
        None
    """
    data = {
            "dcm2bids": {
                "repo": "cbedetti/Dcm2Bids",
                "host": "https://github.com",
                "current": __version__,
                },
            "dcm2niix": {
                "repo": "rordenlab/dcm2niix",
                "host": "https://github.com",
                "current": dcm2niix_version,
                },
            }

    if internet() and is_tool("curl"):
        host = data.get(name)["host"]

        if host == "https://github.com":
            repo = data.get(name)["repo"]
            latest = check_github_latest(repo)

        else:
            #Not implemented
            return

    else:
        logger.debug(
                "Checking latest version of {} was not possible".format(name))
        logger.debug("internet: {}, curl: {}".format(
            internet(), is_tool("curl")))
        return

    current = data.get(name)["current"]
    if callable(current):
        current = current()

    try:
        news = LooseVersion(latest) > LooseVersion(current)
    except:
        news = None

    if news:
        logger.warning("Your using {} version {}".format(name, current))
        logger.warning("A new version exists : {}".format(latest))
        logger.warning("Check {}/{}".format(host, repo))


def dcm2niix_version():
    """
    Returns:
        A string of the version of dcm2niix install on the system
    """
    if not is_tool("dcm2niix"):
        logger.error("dcm2niix is not in your PATH or not installed")
        logger.error("Check https://github.com/rordenlab/dcm2niix")
        return

    try:
        output = check_output(shlex.split("dcm2niix"))
    except:
        logger.error("Running: dcm2niix", exc_info=True)
        return

    try:
        lines = output.decode().split("\n")
    except:
        logger.debug(output, exc_info=True)
        return

    for line in lines:
        try:
            splits = line.split()
            return splits[splits.index('version')+1]
        except:
            continue

    return
