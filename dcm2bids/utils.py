# -*- coding: utf-8 -*-


import json
import os
import shutil


def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


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

