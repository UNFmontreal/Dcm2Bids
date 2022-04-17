# -*- coding: utf-8 -*-


import csv
import json
import logging
import os
from pathlib import PurePath
import re
from collections import OrderedDict
from subprocess import check_output


class DEFAULT(object):
    """ Default values of the package"""

    # cli dcm2bids
    cliSession = ""
    cliOutputDir = os.getcwd()
    cliLogLevel = "INFO"

    # dcm2bids.py
    outputDir = cliOutputDir
    session = cliSession  # also Participant object
    clobber = False
    forceDcm2niix = False
    defaceTpl = None
    logLevel = "WARNING"

    # dcm2niix.py
    dcm2niixOptions = "-b y -ba y -z y -f '%3s_%f_%p_%t'"
    dcm2niixVersion = "v1.0.20181125"

    # sidecar.py
    compKeys = ["SeriesNumber", "AcquisitionTime", "SidecarFilename"]
    searchMethod = "fnmatch"
    searchMethodChoices = ["fnmatch", "re"]
    runTpl = "_run-{:02d}"
    caseSensitive = True

    # Entity table:
    # https://bids-specification.readthedocs.io/en/v1.7.0/99-appendices/04-entity-table.html
    entityTableKeys = ["sub", "ses", "task", "acq", "ce", "rec", "dir",
                       "run", "mod", "echo", "flip", "inv", "mt", "part",
                       "recording"]

    # misc
    tmpDirName = "tmp_dcm2bids"
    helperDir = "helper"


def load_json(filename):
    """ Load a JSON file

    Args:
        filename (str): Path of a JSON file

    Return:
        Dictionnary of the JSON file
    """
    with open(filename, "r") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    return data


def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def write_txt(filename, lines):
    with open(filename, "a") as f:
        for row in lines:
            f.write("%s\n" % row)


def write_participants(filename, participants):
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, delimiter="\t", fieldnames=participants[0].keys())
        writer.writeheader()
        writer.writerows(participants)


def read_participants(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return [row for row in reader]


def splitext_(path, extensions=None):
    """ Split the extension from a pathname
    Handle case with extensions with '.' in it

    Args:
        path (str): A path to split
        extensions (list): List of special extensions

    Returns:
        (root, ext): ext may be empty
    """
    if extensions is None:
        extensions = [".nii.gz"]

    for ext in extensions:
        if path.endswith(ext):
            return path[: -len(ext)], path[-len(ext) :]
    return os.path.splitext(path)


def run_shell_command(commandLine):
    """ Wrapper of subprocess.check_output
    Returns:
        Run command with arguments and return its output
    """
    logger = logging.getLogger(__name__)
    logger.info("Running %s", commandLine)
    return check_output(commandLine)


def valid_path(in_path):
    """Assert that file exists.

    Parameters
    ----------
    required_file: string path
        Path to be checked.
    """
    valid_path = re.sub(r'\\', os.path.sep, in_path)
    valid_path = re.sub(r'\/', os.path.sep, valid_path)
    valid_path = str(PurePath(valid_path))

    if os.path.isfile(valid_path) or os.path.isdir(valid_path):
        if os.path.exists(valid_path):
            return valid_path
    raise FileNotFoundError(in_path)
