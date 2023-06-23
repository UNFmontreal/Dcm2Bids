# -*- coding: utf-8 -*-


import csv
import logging
import os
from pathlib import Path
from subprocess import check_output


class DEFAULT(object):
    """ Default values of the package"""

    doc = "Documentation at https://unfmontreal.github.io/Dcm2Bids/"

    link_bids_validator = "https://github.com/bids-standard/bids-validator#quickstart"
    link_doc_intended_for = "https://unfmontreal.github.io/Dcm2Bids/docs/tutorial/first-steps/#populating-the-config-file"

    # cli dcm2bids
    cliSession = ""
    cliOutputDir = os.getcwd()
    cliLogLevel = "INFO"

    # dcm2bids.py
    outputDir = Path.cwd()
    session = ""  # also Participant object
    bids_validate = False
    auto_extract_entities = False
    clobber = False
    forceDcm2niix = False
    defaceTpl = None
    logLevel = "WARNING"

    entity_dir = {"j-": "AP",
                  "j": "PA",
                  "i-": "LR",
                  "i": "RL",
                  "AP": "AP",
                  "PA": "PA",
                  "LR": "LR",
                  "RL": "RL"}

    # dcm2niix.py
    dcm2niixOptions = "-b y -ba y -z y -f '%3s_%f_%p_%t'"

    # sidecar.py
    auto_extractors = {'SeriesDescription': ["task-(?P<task>[a-zA-Z0-9]+)"],
                       'PhaseEncodingDirection': ["(?P<dir>(j|i)-?)"],
                       'EchoNumber': ["(?P<echo>[0-9])"]}

    extractors = {}

    auto_entities = {"anat_MEGRE": ["echo"],
                     "anat_MESE": ["echo"],
                     "func_cbv": ["task"],
                     "func_bold": ["task"],
                     "func_sbref": ["task"],
                     "fmap_epi": ["dir"]}

    compKeys = ["SeriesNumber", "AcquisitionTime", "SidecarFilename"]
    searchMethodChoices = ["fnmatch", "re"]
    searchMethod = "fnmatch"
    runTpl = "_run-{:02d}"
    caseSensitive = True

    # Entity table:
    # https://bids-specification.readthedocs.io/en/v1.8.0/99-appendices/04-entity-table.html
    entityTableKeys = ["sub", "ses", "task", "acq", "ce", "rec", "dir",
                       "run", "mod", "echo", "flip", "inv", "mt", "part",
                       "recording"]

    # misc
    tmpDirName = "tmp_dcm2bids"
    helperDir = "helper"

    # BIDS version
    bids_version = "v1.8.0"


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


def convert_dir(dir):
    """ Convert Direction
    Args:
        dir (str): direction - dcm format

    Returns:
        str: direction - bids format
    """
    return DEFAULT.entity_dir[dir]
