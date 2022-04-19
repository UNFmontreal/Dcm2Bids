#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore
# pylint: disable=exec-used

"""Setup file for the dcm2bids package"""

import os
import os.path as op
from setuptools import setup, find_packages


def load_version():
    """Execute dcm2bids.version in a global dictionary"""
    global_dict = {}
    with open(op.join("dcm2bids", "version.py")) as _:
        exec(_.read(), global_dict)
    return global_dict


def install_requires():
    """Get list of required modules"""
    required = []
    for module, meta in _VERSION["REQUIRED_MODULE_METADATA"]:
        required.append("{}>={}".format(module, meta["min_version"]))
    return required


_VERSION = load_version()
DISTNAME = "dcm2bids"
VERSION = _VERSION["__version__"]
ENTRY_POINTS = {
    "console_scripts": [
        "dcm2bids = dcm2bids.dcm2bids:main",
        "dcm2bids_helper = dcm2bids.helper:main",
        "dcm2bids_scaffold = dcm2bids.scaffold:main",
    ],
    # "configurations": [],
}
AUTHOR = "Christophe Bedetti"
AUTHOR_EMAIL = "christophe.bedetti@umontreal.ca"
DESCRIPTION = (
    "Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure"
)
with open("README.md", encoding="utf-8") as _:
    LONG_DESCRIPTION = _.read()
LICENSE = "GPLv3+"
PROJECT_URLS = {
    "Documentation": "https://unfmontreal.github.io/Dcm2Bids",
    "Source Code": "https://github.com/unfmontreal/Dcm2Bids",
}
CLASSIFIERS = [
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Science/Research",
    "Operating System :: MacOS",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: Unix",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Scientific/Engineering :: Medical Science Apps.",
]


if __name__ == "__main__":
    setup(
        name=DISTNAME,
        version=VERSION,
        packages=find_packages(exclude=["tests"]),
        entry_points=ENTRY_POINTS,
        python_requires=">=3.7",
        install_requires=['future>=0.17.1'],
        package_data= {'dcm2bids.data': [op.join("data","*")]},
        data_files=[(op.join("data", "scaffold"),
                    [op.join("data", "scaffold", "CHANGES"),
                     op.join("data", "scaffold", "dataset_description.json"),
                     op.join("data", "scaffold", "participants.json"),
                     op.join("data", "scaffold", "participants.tsv"),
                     op.join("data", "scaffold", "README")])],
        include_package_data=True,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        # keywords="",
        license=LICENSE,
        project_urls=PROJECT_URLS,
        classifiers=CLASSIFIERS
    )
