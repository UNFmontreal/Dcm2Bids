# -*- coding: utf-8 -*-


import json
import os
import shutil
from tempfile import TemporaryDirectory

from bids import BIDSLayout

from dcm2bids import Dcm2bids
from dcm2bids.utils import DEFAULT, load_json


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def compare_json(original_file, converted_file):
    with open(original_file) as f:
        original_json = json.load(f)

    with open(converted_file) as f:
        converted_json = json.load(f)

    converted_json.pop('Dcm2bidsVersion', None)

    return original_json == converted_json


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

    app = Dcm2bids(TEST_DATA_DIR, "01",
                   os.path.join(TEST_DATA_DIR, "config_test.json"),
                   bidsDir.name)
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


def test_caseSensitive_false():
    # Validate caseSensitive false
    bidsDir = TemporaryDirectory()

    tmpSubDir = os.path.join(bidsDir.name, DEFAULT.tmpDirName, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmpSubDir)

    app = Dcm2bids(TEST_DATA_DIR, "01",
                   os.path.join(TEST_DATA_DIR,
                                "config_test_not_case_sensitive_option.json"),
                   bidsDir.name)
    app.run()

    layout = BIDSLayout(bidsDir.name,
                        validate=False,
                        ignore='tmp_dcm2bids')

    path_dwi = os.path.join(bidsDir.name,
                            "sub-01",
                            "dwi",
                            "sub-01_dwi.json")

    path_t1 = os.path.join(bidsDir.name,
                           "sub-01",
                           "anat",
                           "sub-01_T1w.json")

    path_localizer = os.path.join(bidsDir.name,
                                  "sub-01",
                                  "localizer",
                                  "sub-01_run-01_localizer.json")

    original_01_localizer = os.path.join(TEST_DATA_DIR,
                                         "sidecars",
                                         "001_localizer_20100603125600_i00001.json")

    original_02_localizer = os.path.join(TEST_DATA_DIR,
                                         "sidecars",
                                         "001_localizer_20100603125600_i00002.json")

    original_03_localizer = os.path.join(TEST_DATA_DIR,
                                         "sidecars",
                                         "001_localizer_20100603125600_i00003.json")

    # Input T1 is UPPER CASE (json)
    json_t1 = layout.get(subject='01',
                         datatype='anat',
                         extension='json',
                         suffix='T1w')

    # Input localizer is lowercase (json)
    json_01_localizer = layout.get(subject='01',
                                   extension='json',
                                   suffix='localizer',
                                   run='01')

    json_02_localizer = layout.get(subject='01',
                                   extension='json',
                                   suffix='localizer',
                                   run='02')

    json_03_localizer = layout.get(subject='01',
                                   extension='json',
                                   suffix='localizer',
                                   run='03')

    # Asking for something with low and up cases (config file)
    json_dwi = layout.get(subject='01',
                          datatype='dwi',
                          extension='json',
                          suffix='dwi')

    assert set(os.listdir(os.path.join(bidsDir.name,
                                       'sub-01'))) == {'anat',
                                                       'dwi',
                                                       'localizer'}
    assert json_t1[0].path == path_t1
    assert json_01_localizer[0].path == path_localizer
    assert json_dwi[0].path == path_dwi

    # Check order runs when same number
    # i00001 no AcquisitionTime
    # i00002 AcquisitionTime after i00003
    assert compare_json(original_01_localizer,
                        json_01_localizer[0].path)
    assert compare_json(original_02_localizer,
                        json_03_localizer[0].path)
    assert compare_json(original_03_localizer,
                        json_02_localizer[0].path)
