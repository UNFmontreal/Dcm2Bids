# -*- coding: utf-8 -*-


import os
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


def print_to_console(message, color):
    print('')
    print('{}{}{}'.format(color, message, bcolors.ENDC))


def ok(message):
    print_to_console(message, bcolors.OKGREEN)


def fail(message):
    print_to_console(message, bcolors.FAIL)


def info(message):
    print_to_console(message, bcolors.OKBLUE)


def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)
