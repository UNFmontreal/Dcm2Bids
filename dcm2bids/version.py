# -*- coding: utf-8 -*-

"""This module take care of the versioning"""

# dcm2bids version
__version__ = "2.1.7"


import logging
import shlex
from distutils.version import LooseVersion
from subprocess import check_output, CalledProcessError, TimeoutExpired
from shutil import which


logger = logging.getLogger(__name__)


def is_tool(name):
    """ Check if a program is in PATH

    Args:
        name (string): program name
    Returns:
        boolean
    """
    return which(name) is not None


def check_github_latest(githubRepo, timeout=3):
    """ Check the latest version of a github repository

    Args:
        githubRepo (string): a github repository ("username/repository")
        timeout (int): time in seconds

    Returns:
        A string of the version
    """
    url = "https://github.com/{}/releases/latest".format(githubRepo)
    try:
        output = check_output(shlex.split("curl -L --silent " + url), timeout=timeout)
    except CalledProcessError:
        logger.info(f"Checking latest version of {githubRepo} was not possible")
        logger.debug(f"Error while 'curl --silent {url}'", exc_info=True)
        return
    except TimeoutExpired:
        logger.info(f"Checking latest version of {githubRepo} was not possible")
        logger.debug(f"Command 'curl --silent {url}' timed out after {timeout}s")
        return
    # The output should have this format
    # <html><body>You are being <a href="https://github.com/{gitRepo}/releases/tag/{version}">redirected</a>.</body></html>
    try:
        version = output.decode().split("{}/releases/tag/".format(githubRepo))[1].split('"')[0]

        # Versions are X.X.X
        if len(version) > 5:
            version = version[:5]
        return version
    except:
        logger.debug(
            "Checking latest version of %s was not possible", githubRepo,
            exc_info=True,
        )
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
            "repo": "unfmontreal/Dcm2Bids",
            "host": "https://github.com",
            "current": __version__,
        },
        "dcm2niix": {
            "repo": "rordenlab/dcm2niix",
            "host": "https://github.com",
            "current": dcm2niix_version,
        },
    }

    if is_tool("curl"):
        host = data.get(name)["host"]

        if host == "https://github.com":
            repo = data.get(name)["repo"]
            latest = check_github_latest(repo)

        else:
            # Not implemented
            return

    else:
        logger.debug("Checking latest version of %s was not possible", name)
        logger.debug("curl: %s", is_tool("curl"))
        return

    current = data.get(name)["current"]
    if callable(current):
        current = current()

    try:
        news = LooseVersion(latest) > LooseVersion(current)
    except:
        news = None

    if news:
        logger.warning("Your using %s version %s", name, current)
        logger.warning("A new version exists : %s", latest)
        logger.warning("Check %s/%s", host, repo)


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
            return splits[splits.index("version") + 1]
        except:
            continue

    return
