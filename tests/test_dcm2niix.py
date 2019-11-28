# -*- coding: utf-8 -*-


import os
import pytest
from dcm2bids.dcm2niix import Dcm2niix
from dcm2bids.utils import DEFAULT
from glob import glob

try:
    from tempfile import TemporaryDirectory
except:
    #python2 compatibility
    from backports.tempfile import TemporaryDirectory


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def test_dcm2niix_run():
    dicomDir = os.path.join(TEST_DATA_DIR, "sourcedata", "sub-01")
    tmpBase = os.path.join(TEST_DATA_DIR, "tmp")

    #tmpDir = TemporaryDirectory(dir=tmpBase)
    tmpDir = TemporaryDirectory()

    app = Dcm2niix([dicomDir], tmpDir.name)
    app.run()

    helperDir = os.path.join(
            tmpDir.name, DEFAULT.tmpDirName, DEFAULT.helperDir, "*")
    ls = sorted(glob(helperDir))
    firstMtime = [os.stat(_).st_mtime for _ in ls]
    assert 'localizer_20100603125600' in ls[0]

    #files should not be change after a rerun
    app.run()
    secondMtime = [os.stat(_).st_mtime for _ in ls]
    assert firstMtime == secondMtime

    #files should be change after a forced rerun
    app.run(force=True)
    thirdMtime = [os.stat(_).st_mtime for _ in ls]
    assert firstMtime != thirdMtime

    tmpDir.cleanup()
