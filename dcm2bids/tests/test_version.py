# -*- coding: utf-8 -*-


import os
import pytest
from dcm2bids.version import internet, is_tool, check_github_latest, __version__


def test_internet():
    assert internet(port=1234) == False


def test_is_tool():
    assert is_tool("dcm2bids")


def test_latest():
    assert check_github_latest("cbedetti/Dcm2Bids") == __version__
