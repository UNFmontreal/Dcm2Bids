# -*- coding: utf-8 -*-


from dcm2bids.version import is_tool, check_github_latest, __version__


def test_is_tool():
    assert is_tool("dcm2bids")
