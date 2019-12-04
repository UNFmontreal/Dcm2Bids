# -*- coding: utf-8 -*-

"""
dcm2bids
--------

Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure
"""


from .dcm2bids import Dcm2bids
from .version import __version__

__all__ = ["Dcm2bids", "__version__"]
