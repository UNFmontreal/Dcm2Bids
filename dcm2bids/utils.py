# -*- coding: utf-8 -*-


import json
import os
import shutil
import csv
from collections import OrderedDict

def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def write_txt(filename,lines=[]):
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
        reader = csv.reader(f, delimiter='\t')
        header = reader.next();
        return [OrderedDict(zip(header,row)) for row in reader]

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

