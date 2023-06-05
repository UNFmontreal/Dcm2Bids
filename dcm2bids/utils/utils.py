# -*- coding: utf-8 -*-


import csv
import json
import logging
import os
from pathlib import Path
import re
from collections import OrderedDict
import shlex
import shutil
from subprocess import check_output


class DEFAULT(object):
    """ Default values of the package"""

    doc = "Documentation at https://unfmontreal.github.io/Dcm2Bids/"

    # cli dcm2bids
    cliSession = ""
    cliOutputDir = os.getcwd()
    cliLogLevel = "INFO"

    # dcm2bids.py
    outputDir = cliOutputDir
    session = ""  # also Participant object
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


def valid_path(in_path, type="folder"):
    """Assert that file exists.

    Parameters
    ----------
    required_file: Path
        Path to be checked.
    """
    if isinstance(in_path, str):
        in_path = Path(in_path)

    if type == 'folder':
        if in_path.is_dir() or in_path.parent.is_dir():
            return in_path
        else:
            raise NotADirectoryError(in_path)
    elif type == "file":
        if in_path.is_file():
            return in_path
        else:
            raise FileNotFoundError(in_path)

    raise TypeError(type)


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
