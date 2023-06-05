# -*- coding: utf-8 -*-


import csv
import inspect
import json
import logging
import os
import os.path as op
from collections import OrderedDict
import shlex
import shutil
from subprocess import check_output

import dcm2bids


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
    with filename.open("w") as f:
        json.dump(data, f, indent=4)


def write_txt(filename, lines):
    with open(filename, "a") as f:
        for row in lines:
            f.write("%s\n" % row)


def run_shell_command(commandLine):
    """ Wrapper of subprocess.check_output
    Returns:
        Run command with arguments and return its output
    """
    logger = logging.getLogger(__name__)
    logger.info("Running %s", commandLine)
    return check_output(commandLine)


def get_scaffold_dir():
    """
    Return SCAFFOLD data directory in dcm2bids repository

    Returns
    -------
    scaffold_dir: string
        SCAFFOLD path
    """

    module_path = os.path.dirname(os.path.dirname(inspect.getfile(dcm2bids)))
    # module_path = inspect.getfile(dcm2bids)
    scaffold_dir = opj(module_path, 'data', 'scaffold')
    # scaffold_dir = pkg_resources.resource_filename(__name__,  os.path.join("data", "scaffold"))
    # print(module_path)
    # scaffold_dir = os.path.join(os.path.dirname(
    # os.path.dirname(module_path)), "data", "scaffold")

    print(scaffold_dir)
    return scaffold_dir