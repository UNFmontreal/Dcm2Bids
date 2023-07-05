# -*- coding: utf-8 -*-

from tempfile import TemporaryDirectory
import os


def test_help_option(script_runner):
    ret = script_runner.run(['dcm2bids_scaffold', '--help'])
    assert ret.success


def test_run_scaffold(script_runner):
    bids_dir = TemporaryDirectory()
    scaffold_dir = os.path.join(bids_dir.name, "scaffold_dir")
    ret = script_runner.run(['dcm2bids_scaffold', '-o', scaffold_dir])
    assert ret.success

    ret = script_runner.run(['dcm2bids_scaffold', '-o', scaffold_dir, '--force'])
    assert ret.success
