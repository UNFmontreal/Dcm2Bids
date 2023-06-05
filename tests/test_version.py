# -*- coding: utf-8 -*-


from dcm2bids.utils.tools import is_tool


def test_is_tool():
    assert is_tool("dcm2bids")
