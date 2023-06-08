# -*- coding: utf-8 -*-

import pytest


def test_help_option(script_runner):
    ret = script_runner.run(['dcm2bids_scaffold', '--help'])
    assert ret.success

def test_run_scaffold(script_runner):
    ret = script_runner.run(['dcm2bids_scaffold', '-o', 'o_scaffold', '--force'])
    assert ret.success
