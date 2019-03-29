# -*- coding: utf-8 -*-


import csv
import json
import logging
import os
import shlex
from collections import OrderedDict
from subprocess import check_output, CalledProcessError


class DEFAULT(object):
    """ Default values of the package"""
    #cli dcm2bids
    cliSession = ""
    cliOutputDir = os.getcwd()
    cliLogLevel = "INFO"

    #dcm2bids.py
    outputDir = cliOutputDir
    session = cliSession #also Participant object
    clobber = False
    forceDcm2niix = False
    defaceTpl = None
    logLevel = "WARNING"

    #dcm2niix.py
    dcm2niixOptions = "-b y -ba y -z y -f '%3s_%f_%p_%t'"
    dcm2niixVersion = "v1.0.20181125"

    #sidecar.py
    compKeys = ["SeriesNumber", "AcquisitionTime", "SidecarFilename"]
    searchMethod = "fnmatch"
    searchMethodChoices = ["fnmatch", "re"]
    runTpl = "_run-{:02d}"

    #misc
    tmpDirName = "tmp_dcm2bids"
    helperDir = "helper"


def load_json(filename):
    """ Load a JSON file

    Args:
        filename (str): Path of a JSON file

    Return:
        Dictionnary of the JSON file
    """
    with open(filename, 'r') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    return data


def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def write_txt(filename, lines=[]):
    with open(filename, 'a') as f:
        for row in lines:
            f.write("%s\n" % row)


def write_participants(filename,participants):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, delimiter='\t',
                                fieldnames=participants[0].keys())
        writer.writeheader()
        writer.writerows(participants)


def read_participants(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        return [row for row in reader]


def splitext_(path, extensions=['.nii.gz']):
    """ Split the extension from a pathname
    Handle case with extensions with '.' in it

    Args:
        path (str): A path to split
        extensions (list): List of special extensions

    Returns:
        (root, ext): ext may be empty
    """
    for ext in extensions:
        if path.endswith(ext):
            return path[:-len(ext)], path[-len(ext):]
    return os.path.splitext(path)


def run_shell_command(commandLine):
    """ Wrapper of subprocess.check_output

    Returns:
        Run command with arguments and return its output
    """
    logger = logging.getLogger(__name__)
    logger.info("Running {}".format(commandLine))
    return check_output(shlex.split(commandLine))

