# -*- coding: utf-8 -*-

from os.path import join as opj
from os import path
from setuptools import setup, find_packages

# Get version and release info, which is all stored in dcm2bids/version.py
ver_file = opj('dcm2bids', 'version.py')
with open(ver_file) as f:
    exec(f.read())

# Long description will go up on the pypi page
here = path.abspath(path.dirname(__file__))

with open(opj(here, "README.md"), encoding="utf-8") as _:
    LONG_DESCRIPTION = _.read()

opts = dict(name=NAME,
            maintainer=MAINTAINER,
            maintainer_email=MAINTAINER_EMAIL,
            description=DESCRIPTION,
            long_description=LONG_DESCRIPTION,
            long_description_content_type="text/markdown",
            project_urls=PROJECT_URLS,
            license=LICENSE,
            classifiers=CLASSIFIERS,
            platforms=PLATFORMS,
            python_requires=">3.7",
            install_requires=['packaging>=23.1'],
            version=VERSION,
            packages=find_packages(exclude=["tests"]),
            entry_points=ENTRY_POINTS)


setup(**opts)
