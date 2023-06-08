# -*- coding: utf-8 -*-

import inspect
import json
import os
import os.path as opj
from pathlib import Path
from collections import OrderedDict

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
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def write_txt(filename, lines):
    with open(filename, "a+") as f:
        f.write(f"{lines}\n")


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
