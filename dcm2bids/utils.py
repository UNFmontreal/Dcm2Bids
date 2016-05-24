# -*- coding: utf-8 -*-


import dicom
from dicom.errors import InvalidDicomError
import json
import os


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
