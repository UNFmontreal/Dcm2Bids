# -*- coding: utf-8 -*-


from dcm2bids.version import internet, is_tool, check_github_latest, __version__


def test_internet():
    assert internet(port=1234) is False


def test_is_tool():
    assert is_tool("dcm2bids")
