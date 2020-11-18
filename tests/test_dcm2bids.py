# -*- coding: utf-8 -*-


import os
import shutil
from tempfile import TemporaryDirectory
from bids import BIDSLayout
from dcm2bids import Dcm2bids
from dcm2bids.utils import DEFAULT, load_json


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def test_dcm2bids():
    # tmpBase = os.path.join(TEST_DATA_DIR, "tmp")
    # bidsDir = TemporaryDirectory(dir=tmpBase)
    bidsDir = TemporaryDirectory()

    tmpSubDir = os.path.join(bidsDir.name, DEFAULT.tmpDirName, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmpSubDir)

    app = Dcm2bids(
        [TEST_DATA_DIR],
        "01",
        os.path.join(TEST_DATA_DIR, "config_test.json"),
        bidsDir.name,
    )
    app.run()
    layout = BIDSLayout(bidsDir.name, validate=False)

    assert layout.get_subjects() == ["01"]
    assert layout.get_sessions() == []
    assert layout.get_tasks() == ["rest"]
    assert layout.get_runs() == [1, 2, 3]

    app = Dcm2bids(
        [TEST_DATA_DIR],
        "01",
        os.path.join(TEST_DATA_DIR, "config_test.json"),
        bidsDir.name,
    )
    app.run()

    fmapFile = os.path.join(bidsDir.name, "sub-01", "fmap", "sub-01_echo-492_fmap.json")
    data = load_json(fmapFile)
    fmapMtime = os.stat(fmapFile).st_mtime
    assert data["IntendedFor"] == "dwi/sub-01_dwi.nii.gz"

    data = load_json(
        os.path.join(
            bidsDir.name, "sub-01", "localizer", "sub-01_run-01_localizer.json"
        )
    )
    assert data["ProcedureStepDescription"] == "Modify by dcm2bids"

    # rerun
    shutil.rmtree(tmpSubDir)
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmpSubDir)

    app = Dcm2bids(
        [TEST_DATA_DIR],
        "01",
        os.path.join(TEST_DATA_DIR, "config_test.json"),
        bidsDir.name,
    )
    app.run()

    fmapMtimeRerun = os.stat(fmapFile).st_mtime
    assert fmapMtime == fmapMtimeRerun

    if os.name != 'nt':
        bidsDir.cleanup()

def test_caseSensitive_false():
    # Validate caseSensitive false
    bidsDir = TemporaryDirectory()

    tmpSubDir = os.path.join(bidsDir.name, DEFAULT.tmpDirName, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmpSubDir)

    app = Dcm2bids(
        [TEST_DATA_DIR],
        "01",
        os.path.join(TEST_DATA_DIR,
                     "config_test_not_case_sensitive_option.json"),
                     bidsDir.name)
    app.run()

    layout = BIDSLayout(bidsDir.name,
                        validate=False,
                        ignore='tmp_dcm2bids')

    # Input T1 is UPPER CASE (json)
    json_t1 = layout.get(subject='01',
                         datatype='anat',
                         extension='json',
                         suffix='T1w')

    # Input  localizer is lowercase (json)
    json_localizer = layout.get(subject='01',
                                extension='json',
                                suffix='localizer')

    # Asking for something with low and up cases (config file)
    json_dwi = layout.get(subject='01',
                          datatype='dwi',
                          extension='json',
                          suffix='dwi')

    path_t1 = os.path.join(bidsDir.name,
                           "sub-01",
                           "anat",
                           "sub-01_T1w.json")

    path_localizer = os.path.join(bidsDir.name,
                                  "sub-01",
                                  "localizer",
                                  "sub-01_run-01_localizer.json")

    path_dwi = os.path.join(bidsDir.name,
                            "sub-01",
                            "dwi",
                            "sub-01_dwi.json")

    assert layout.get_subjects() == ["01"]
    assert json_t1[0].path == path_t1
    assert json_localizer[0].path == path_localizer
    assert json_dwi[0].path == path_dwi

    if os.name != 'nt':
        bidsDir.cleanup()
