# -*- coding: utf-8 -*-


import json
import os
import shutil
import csv


def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
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


def make_directory_tree(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def clean(directory):
    make_directory_tree(directory)
    if not os.listdir(directory) == []:
        shutil.rmtree(directory)
        make_directory_tree(directory)
    else:
        make_directory_tree(directory)


def splitext_(path):
    for ext in ['.nii.gz']:
        if path.endswith(ext):
            return path[:-len(ext)], path[-len(ext):]
    return os.path.splitext(path)


def run_shell_command(commandLine):
    import logging
    import shlex
    import subprocess

    logger = logging.getLogger("dcm2bids")

    cmd = shlex.split(commandLine)
    logger.info("subprocess: {}".format(commandLine))

    try:
        process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, _ = process.communicate()

        try:
            logger.info("\n" + output.decode("utf-8"))
        except:
            logger.info(output)

    except OSError as exception:
        logger.error("Exception: {}".format(exception))
        logger.info("subprocess failed")

