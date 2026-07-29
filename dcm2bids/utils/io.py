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


def update_participants_tsv(bids_dir, participant_name, logger):
    """Add a participant name to the participants.tsv file.

    Creates the participants.tsv file if it doesn't exist, and adds the
    participant name if not already present.

    Args:
        bids_dir (str or Path): Path to the BIDS directory
        participant_name (str): Name of the participant (e.g., 'sub-01')
        logger: Logger object for logging messages
    """
    if isinstance(bids_dir, str):
        bids_dir = Path(bids_dir)

    participants_file = bids_dir / "participants.tsv"
    existing_participants = set()

    # Read existing participants if file exists
    if participants_file.exists():
        with open(participants_file, "r") as f:
            lines = f.readlines()
            # Skip header line (participant_id)
            if len(lines) > 1:
                existing_participants = {line.split()[0] for line in lines[1:] if line.strip()}
    else:
        logger.info("Creating new participants.tsv file")

    # Add participant if not already present
    if participant_name not in existing_participants:
        existing_participants.add(participant_name)
        logger.info(f"Adding participant '{participant_name}' to participants.tsv")

        # Write participants.tsv with sorted participant IDs
        with open(participants_file, "w") as f:
            f.write("participant_id\n")
            for participant in sorted(existing_participants):
                f.write(f"{participant}\n")
    else:
        logger.info(f"Participant '{participant_name}' already in participants.tsv")
