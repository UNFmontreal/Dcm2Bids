# -*- coding: utf-8 -*-


import csv
import logging
import os
import datetime
from pathlib import Path
from subprocess import Popen, PIPE

from dcm2bids.version import __version__, __BIDSversion__
from dcm2bids.utils.schema import load_schema_derived_defaults



class DEFAULT(object):
    """ Default values of the package"""

    doc = "Documentation at https://unfmontreal.github.io/Dcm2Bids/"

    link_bids_validator = "https://github.com/bids-standard/bids-validator#quickstart"
    link_doc_intended_for = f"https://unfmontreal.github.io/Dcm2Bids/{__version__}/tutorial/first-steps/#populating-the-config-file"  # noqa: E501

    # cli dcm2bids
    cli_session = ""
    cli_log_level = "INFO"

    bids_version = __BIDSversion__

    # Archives
    arch_extensions = "tar, tar.bz2, tar.gz or zip"

    # dcm2bids.py
    output_dir = Path.cwd()
    session = ""  # also Participant object
    bids_validate = False
    auto_extract_entities = False
    do_not_reorder_entities = False
    clobber = False
    force_dcm2bids = False
    post_op = []
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
    skip_dcm2niix = False

    # sidecar.py
    extractors = {}
    auto_extractors = {'SeriesDescription': ["task-(?P<task>[a-zA-Z0-9]+)"],
                       'PhaseEncodingDirection': ["(?P<dir>(j|i)-?)"],
                       'EchoNumber': ["(?P<echo>[0-9])"]}

    # Compute schema-derived defaults once from the default schema.
    _SCHEMA_DERIVED = load_schema_derived_defaults()
    # Default schema-derived entity table keys derived from it.
    # If schema loading fails, dcm2bids will raise at import time
    entityTableKeys = _SCHEMA_DERIVED["entity_table_keys"]

    # Default schema-derived auto entities.
    auto_entities = _SCHEMA_DERIVED["auto_entities"]

    compKeys = ["AcquisitionTime", "SeriesNumber", "SidecarFilename"]
    search_methodChoices = ["fnmatch", "re"]
    search_method = "fnmatch"
    dup_method_choices = ["dup", "run"]
    dup_method = "run"
    runTpl = "_run-{:02d}"
    dupTpl = "_dup-{:02d}"
    bids_uri_choices = ["URI", "relative"]
    bids_uri = "URI"
    case_sensitive = True

    keyWithPathsidecar_changes = ['IntendedFor', 'Sources']

    # misc
    tmp_dir_name = "tmp_dcm2bids"
    helper_dir = "helper"

    old_keys = ["dataType", "modalityLabel", "customLabels",
                "sidecarChanges", "intendedFor"]


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


def normalize_acquisition_time(value):
    """
    Normalize acquisition time strings into a tuple
    (hour, minute, second, microsecond).

    Accepts both colon-separated times (H:M:S[.fraction]) and compact
    HHMMSS[.fraction]. Returns the original value if it cannot be parsed.
    """
    if not isinstance(value, str):
        return value

    s = value.strip()

    # Try a small set of strict formats using only datetime.strptime
    for fmt in ("%H:%M:%S.%f", "%H:%M:%S", "%H%M%S.%f", "%H%M%S"):
        try:
            dt = datetime.datetime.strptime(s, fmt)
            return (dt.hour, dt.minute, dt.second, dt.microsecond)
        except ValueError:
            continue

    return value


def run_shell_command(commandLine, log=True):
    """ Wrapper of subprocess.check_output
    Returns:
        Run command with arguments and return its output
    """
    if log:
        logger = logging.getLogger(__name__)
        logger.info("Running: %s", " ".join(str(item) for item in commandLine))

    pipes = Popen(commandLine, stdout=PIPE, stderr=PIPE)
    std_out, std_err = pipes.communicate()

    return std_out


def convert_dir(dir):
    """ Convert Direction
    Args:
        dir (str): direction - dcm format

    Returns:
        str: direction - bids format
    """
    return DEFAULT.entity_dir[dir]


def combine_dict_extractors(d1, d2):
    """ combine dict
    Args:
        d1 (dic): dictionary
        d2 (dic): dictionary

    Returns:
        dict: dictionary with combined information
              if d1 d2 use the same keys, return dict will return a list of items.
    """
    return {
            k: [d[k][0] for d in (d1, d2) if k in d]
            for k in set(d1.keys()) | set(d2.keys())
        }


class TreePrinter:
    """
    Generates and prints a tree representation of a given a directory.
    """

    BRANCH = "│"
    LAST = "└──"
    JUNCTION = "├──"
    BRANCH_PREFIX = "│   "
    SPACE = "    "

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

    def print_tree(self):
        """
        Prints the tree representation of the root directory and
        its subdirectories and files.
        """
        tree = self._generate_tree(self.root_dir)
        logger = logging.getLogger(__name__)
        logger.info(f"Tree representation of {self.root_dir}{os.sep}")
        logger.info(f"{self.root_dir}{os.sep}")
        for item in tree:
            logger.info(item.encode("utf-8", errors="ignore").decode("utf-8"))

    def _generate_tree(self, directory, prefix=""):
        """
        Generates the tree representation of the <directory> recursively.

        Parameters:
        - directory: Path
            The directory for which a tree representation is needed.
        - prefix: str
            The prefix to be added to each entry in the tree.

        Returns a list of strings representing the tree.
        """
        tree = []
        entries = sorted(directory.iterdir(), key=lambda path: str(path).lower())
        entries = sorted(entries, key=lambda entry: entry.is_file())
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            connector = self.LAST if index == entries_count - 1 else self.JUNCTION
            if entry.is_dir():
                sub_tree = self._generate_tree(
                    entry,
                    prefix=prefix
                    + (
                        self.BRANCH_PREFIX if index != entries_count - 1 else self.SPACE
                    ),
                )
                tree.append(f"{prefix}{connector} {entry.name}{os.sep}")
                tree.extend(sub_tree)
            else:
                tree.append(f"{prefix}{connector} {entry.name}")
        return tree
