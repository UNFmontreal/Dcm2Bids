# -*- coding: utf-8 -*-

import json
from pathlib import Path
from collections import OrderedDict


def load_json(filename):
    """ Load a JSON file

    Args:
        filename (str): Path of a JSON file

    Return:
        Dictionary of the JSON file
    """
    with open(filename, "r") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    return data


def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def write_txt(filename, lines):
    with open(filename, "w") as f:
        f.write(f"{lines}\n")


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
