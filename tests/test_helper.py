# -*- coding: utf-8 -*-

import pytest


def test_help_option(script_runner):
    ret = script_runner.run(['dcm2bids_helper', '--help'])
    assert ret.success
