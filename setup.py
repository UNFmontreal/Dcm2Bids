#!/usr/bin/env python
# -*- coding: utf-8 -*-


import glob
import os
from setuptools import setup


#Get __version__ from dcm2bids.version
exec(open(os.path.join("dcm2bids", "version.py")).read())


description = """Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure
                 this is a fork of  Dcm2Bids @ https://github.com/cbedetti/Dcm2Bids created 
                 for DCAN labs at OHSU that allows the user to choose which compression
                 is used in the conversion of Dicoms to Nifti's/Bids. This fork was created
                 from cbedetti commit 86a7be97149e3a5f31b3b75bc8c9e68e005a99dc"""


try:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except:
    #python2 compatibility
    from io import open
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()


DISTNAME = "dcan-labs-dcm2bids"
DESCRIPTION = description
VERSION = __version__
AUTHOR = "Anthony Galassi"
AUTHOR_EMAIL = "anthony.e.galassi@gmail.com"
URL = "https://github.com/bendhouseart/Dcm2Bids"
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
            packages=['dcan-labs-dcm2bids'],
            scripts=glob.glob('scripts/dcm2bids*'),
            install_requires=['future'],
            )
