# -*- coding: utf-8 -*-

from tempfile import TemporaryDirectory


def test_help_option(script_runner):
    ret = script_runner.run(['dcm2bids_helper', '--help'])
    assert ret.success


def test_helper(script_runner):
    i_tmpDir = TemporaryDirectory()
    o_tmpDir = TemporaryDirectory()
    ret = script_runner.run(['dcm2bids_helper', '-d', i_tmpDir.name,
                                                '-o', o_tmpDir.name,
                                                '-n', '--force',
                                                '-l', 'ERROR'])
    assert not ret.success
