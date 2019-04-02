#!/usr/bin/env python
# -*- coding: utf-8 -*-


import glob
import os
from setuptools import setup


#Get __version__ from dcm2bids.version
exec(open(os.path.join("dcm2bids", "version.py")).read())


description = """Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure"""


try:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except:
    #python2 compatibility
    from io import open
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()


DISTNAME = "dcm2bids"
DESCRIPTION = description
VERSION = __version__
AUTHOR = "Christophe Bedetti"
AUTHOR_EMAIL = "christophe.bedetti@umontreal.ca"
URL = "https://github.com/cbedetti/Dcm2Bids"
DOWNLOAD_URL = URL + "/archive/" + VERSION + ".tar.gz"


if __name__ == "__main__":
    setup(
            name=DISTNAME,
            version=VERSION,
            description=description,
            long_description=long_description,
            long_description_content_type='text/markdown',
            author=AUTHOR,
            author_email=AUTHOR_EMAIL,
            url=URL,
            download_url=DOWNLOAD_URL,
            packages=['dcm2bids'],
            scripts=glob.glob('scripts/dcm2bids*'),
            install_requires=['future'],
            )
