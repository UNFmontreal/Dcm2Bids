# -*- coding: utf-8 -*-

"""This module checks whether a software is in PATH, for version, and for updates."""

import logging
import json
from urllib import error, request
from subprocess import getoutput
from shutil import which
from dcm2bids.version import __version__

logger = logging.getLogger(__name__)


def is_tool(name):
    """ Check if a program is in PATH

    Args:
        name (string): program name
    Returns:
        boolean
    """
    return which(name) is not None


def check_github_latest(github_repo, timeout=3):
    """
    Check the latest version of a github repository. Will skip the process if
    no connection can be established.

    Args:
        githubRepo (string): a github repository ("username/repository")
        timeout (int): time in seconds

    Returns:
        A string of the latest release tag that correspond to the version
    """
    req = request.Request(
      url=f"https://api.github.com/repos/{github_repo}/releases/latest")
    try:
        response = request.urlopen(req, timeout=timeout)
    except error.HTTPError as e:
        logger.warning(f"Checking latest version of {github_repo} was not possible, "
                       "the server couldn't fulfill the request.")
        logger.debug(f"Error code: {e.code}")
        return "no_internet"
    except error.URLError as e:
        logger.warning(f"Checking latest version of {github_repo} was not possible, "
                       "your machine is probably not connected to the Internet.")
        logger.debug(f"Reason {e.reason}")
        return "no_internet"
    else:
        content = json.loads(response.read())
        return content["tag_name"]


def check_latest(name="dcm2bids"):
    """ Check if a new version of a software exists and print some details
    Implemented for dcm2bids and dcm2niix

    Args:
        name (string): name of the software

    Returns:
        None
    """
    data = {
        "dcm2bids": {
            "repo": "UNFmontreal/Dcm2Bids",
            "host": "https://github.com",
            "current": __version__,
        },
        "dcm2niix": {
            "repo": "rordenlab/dcm2niix",
            "host": "https://github.com",
            "current": dcm2niix_version,
        },
    }

    repo = data.get(name)["repo"]
    host = data.get(name)["host"]
    current = data.get(name)["current"]
    if callable(current):
        current = current()
    latest = check_github_latest(repo)

    if latest != "no_internet" and latest > current:
        logger.warning(f"A newer version exists for {name}: {latest}")
        logger.warning(f"You should update it -> {host}/{repo}.")
    elif latest != "no_internet":
        logger.info(f"Currently using the latest version of {name}.")


def dcm2niix_version(name="dcm2niix"):
    """
    Check and raises an error if dcm2niix is not in PATH.
    Then check for the version installed.

    Returns:
        A string of the version of dcm2niix install on the system
    """
    if not is_tool(name):
        logger.error(f"{name} is not in your PATH or not installed.")
        logger.error("https://github.com/rordenlab/dcm2niix to troubleshoot.")
        raise FileNotFoundError(f"{name} is not in your PATH or not installed."
                                " -> https://github.com/rordenlab/dcm2niix"
                                " to troubleshoot.")

    try:
        output = getoutput("dcm2niix --version")
    except Exception:
        logger.exception("Checking dcm2niix version", exc_info=False)
        return
    else:
        return output.split()[-1]
