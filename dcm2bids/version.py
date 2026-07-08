# -*- coding: utf-8 -*-

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 3
_version_minor = 2
_version_micro = 0
_version_extra = ''

# Construct full version string from these.
_ver = [_version_major, _version_minor, _version_micro]
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = [
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Science/Research",
    "Operating System :: MacOS",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: Unix",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Scientific/Engineering :: Medical Science Apps.",
]

# Description should be a one-liner:
description = "Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure"

NAME = "dcm2bids"
MAINTAINER = "Arnaud Boré"
MAINTAINER_EMAIL = "arnaud.bore@gmail.com"
DESCRIPTION = description
PROJECT_URLS = {
    "Documentation": "https://unfmontreal.github.io/Dcm2Bids",
    "Source Code": "https://github.com/unfmontreal/Dcm2Bids",
}
LICENSE = "GPLv3+"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
ENTRY_POINTS = {'console_scripts': [
    'dcm2bids=dcm2bids.cli.dcm2bids:main',
    'dcm2bids_helper=dcm2bids.cli.dcm2bids_helper:main',
    'dcm2bids_scaffold=dcm2bids.cli.dcm2bids_scaffold:main',
]}
