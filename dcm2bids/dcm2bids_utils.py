# -*- coding: utf-8 -*-


import os
import dicom
from dicom.errors import InvalidDicomError
import json


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def info(message):
    print('')
    print('{}{}{}'.format(bcolors.OKBLUE, message, bcolors.ENDC))


def getDicomFromDir(directory):
    for f in os.listdir(directory):
        try:
            ds = dicom.read_file(os.path.join(directory, f))
            break
        except InvalidDicomError:
            continue
    return ds


def loadJsonFile(jsonFile):
    with open(jsonFile, 'r') as f:
        data = json.load(f)
    return data


def writingJSON(data, jsonFile):
    with open(jsonFile, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def makedirs(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
