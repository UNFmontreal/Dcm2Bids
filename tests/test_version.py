# -*- coding: utf-8 -*-


from dcm2bids.utils.tools import internet, is_tool


def test_internet():
    assert internet(port=1234) is False


def test_is_tool():
    assert is_tool("dcm2bids")
