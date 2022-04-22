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

    # cli dcm2bids
    cliLogLevel = "INFO"
    EPILOG="Documentation at https://github.com/unfmontreal/Dcm2Bids"

    # dcm2bids.py
    outputDir = Path.cwd()
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

def assert_dirs_empty(parser, args, required):
    """
    Assert that all directories exist are empty.
    If dirs exist and not empty, and --force is used, delete dirs.

    Parameters
    ----------
    parser: argparse.ArgumentParser object
        Parser.
    args: argparse namespace
        Argument list.
    required: string or list of paths to files
        Required paths to be checked.
    create_dir: bool
        If true, create the directory if it does not exist.
    """
    def check(path):
        if not path.is_dir():
            return

        if not any(path.iterdir()):
            return

        if not args.overwrite:
            parser.error(
                f"Output directory {path} isn't empty, so some files "
                "could be overwritten or deleted.\nRerun the command with "
                "--force option to overwrite existing output files.")
        else:
            for the_file in path.iterdir():
                file_path = path / the_file
                try:
                    if file_path.is_file():
                        file_path.unlink()
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(e)

    if isinstance(required, str) or isinstance(required, Path):
        required = [Path(required)]

    for cur_dir in required:
        check(cur_dir)
