# -*- coding: utf-8 -*-


import json
import os
import shutil
import csv
import logging
import shlex
from subprocess import check_output


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


def dcm2niix_version():
    output = run_shell_command("dcm2niix").split()
    try:
        version = output[output.index(b'version')+1]
    except:
        version = None
    return version


def run_shell_command(commandLine):
    """ Wrapper of subprocess.check_output

    Returns:
        Run command with arguments and return its output
    """
    logging.info("Subprocess:{}".format(commandLine))

    output = None
    try:
        output = check_output(shlex.split(commandLine))

        #try:
            #output = output.decode()
        #except:
            #pass

    except FileNotFoundError as e:
        logging.error(e.strerror)
        raise

    #except OSError as e:
        #logging.error(e.strerror)
        #raise

    return output
