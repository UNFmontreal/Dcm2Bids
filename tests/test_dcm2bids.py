# -*- coding: utf-8 -*-


import json
import os
import shutil
from tempfile import TemporaryDirectory

from bids import BIDSLayout

from dcm2bids.dcm2bids_gen import Dcm2BidsGen
from dcm2bids.utils.utils import DEFAULT
from dcm2bids.utils.io import load_json

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def test_help_option(script_runner):
    ret = script_runner.run(['dcm2bids', '--help'])
    assert ret.success


def compare_json(original_file, converted_file):
    with open(original_file) as f:
        original_json = json.load(f)

    with open(converted_file) as f:
        converted_json = json.load(f)

    converted_json.pop('Dcm2bidsVersion', None)

    return original_json == converted_json


def test_dcm2bids_wrong_input(script_runner):

    bids_dir = TemporaryDirectory()
    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    # Wrong participant
    ret_p = script_runner.run(['dcm2bids', '-d', bids_dir,
                               '-p', "01_",
                               '-c',  os.path.join(TEST_DATA_DIR, "config_test.json")])
    assert not ret_p.success

    # Wrong session
    ret_s = script_runner.run(['dcm2bids', '-d', bids_dir,
                               '-p', "01",
                               '-s', "ses-01_",
                               '-c',  os.path.join(TEST_DATA_DIR, "config_test.json")])
    assert not ret_s.success


def test_dcm2bids():
    # tmpBase = os.path.join(TEST_DATA_DIR, "tmp")
    # bids_dir = TemporaryDirectory(dir=tmpBase)
    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR, "config_test.json"),
                      bids_dir.name)
    app.run()

    layout = BIDSLayout(bids_dir.name, validate=False)

    assert layout.get_subjects() == ["01"]
    assert layout.get_sessions() == []
    assert layout.get_tasks() == ["rest"]
    assert layout.get_runs() == [1, 2, 3]

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR, "config_test.json"),
                      bids_dir.name)
    app.run()

    fmapFile = os.path.join(bids_dir.name,
                            "sub-01",
                            "fmap",
                            "sub-01_echo-492_fmap.json")
    data = load_json(fmapFile)
    assert data["IntendedFor"] == ["bids::" + os.path.join("sub-01",
                                                           "dwi",
                                                           "sub-01_dwi.nii.gz"),
                                   "bids::" + os.path.join("sub-01",
                                                           "anat",
                                                           "sub-01_T1w.nii")]

    fmapFile = os.path.join(bids_dir.name,
                            "sub-01",
                            "fmap",
                            "sub-01_echo-738_fmap.json")
    data = load_json(fmapFile)
    fmapMtime = os.stat(fmapFile).st_mtime
    assert data["IntendedFor"] == "bids::" + os.path.join("sub-01",
                                                          "dwi",
                                                          "sub-01_dwi.nii.gz")

    data = load_json(
        os.path.join(
            bids_dir.name, "sub-01", "localizer", "sub-01_run-01_localizer.json"
        )
    )
    assert data["ProcedureStepDescription"] == "Modify by dcm2bids"

    # rerun
    shutil.rmtree(tmp_sub_dir)
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(
        [TEST_DATA_DIR],
        "01",
        os.path.join(TEST_DATA_DIR, "config_test.json"),
        bids_dir.name,
    )
    app.run()

    fmapMtimeRerun = os.stat(fmapFile).st_mtime
    assert fmapMtime == fmapMtimeRerun


def test_dcm2bids_case_sensitive():
    # Validate case_sensitive false
    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR,
                                   "config_test_not_case_sensitive_option.json"),
                      bids_dir.name)
    app.run()

    layout = BIDSLayout(bids_dir.name,
                        validate=False)

    path_dwi = os.path.join(bids_dir.name,
                            "sub-01",
                            "dwi",
                            "sub-01_dwi.json")

    path_t1 = os.path.join(bids_dir.name,
                           "sub-01",
                           "anat",
                           "sub-01_T1w.json")

    path_localizer = os.path.join(bids_dir.name,
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

    assert set(os.listdir(os.path.join(bids_dir.name,
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

    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR, "config_test.json"),
                      bids_dir.name)
    app.run()

    layout = BIDSLayout(bids_dir.name, validate=False)

    assert layout.get_subjects() == ["01"]
    assert layout.get_sessions() == []
    assert layout.get_tasks() == ["rest"]
    assert layout.get_runs() == [1, 2, 3]

    fmapFile = os.path.join(bids_dir.name,
                            "sub-01",
                            "fmap",
                            "sub-01_echo-492_fmap.json")
    data = load_json(fmapFile)
    assert data["IntendedFor"] == ["bids::" + os.path.join("sub-01",
                                                           "dwi",
                                                           "sub-01_dwi.nii.gz"),
                                   "bids::" + os.path.join("sub-01",
                                                           "anat",
                                                           "sub-01_T1w.nii")]

    fmapFile = os.path.join(bids_dir.name,
                            "sub-01",
                            "fmap",
                            "sub-01_echo-738_fmap.json")
    data = load_json(fmapFile)
    fmapMtime = os.stat(fmapFile).st_mtime
    assert data["IntendedFor"] == "bids::" + os.path.join("sub-01",
                                                          "dwi",
                                                          "sub-01_dwi.nii.gz")

    data = load_json(
        os.path.join(
            bids_dir.name, "sub-01", "localizer", "sub-01_run-01_localizer.json"
        )
    )
    assert data["ProcedureStepDescription"] == "Modify by dcm2bids"

    # rerun
    shutil.rmtree(tmp_sub_dir)
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(
        [TEST_DATA_DIR],
        "01",
        os.path.join(TEST_DATA_DIR, "config_test.json"),
        bids_dir.name,
    )
    app.run()

    fmapMtimeRerun = os.stat(fmapFile).st_mtime
    assert fmapMtime == fmapMtimeRerun


def test_dcm2bids_auto_extract():
    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR, "config_test_auto_extract.json"),
                      bids_dir.name,
                      auto_extract_entities=True)
    app.run()

    layout = BIDSLayout(bids_dir.name, validate=False)

    assert layout.get_subjects() == ["01"]
    assert layout.get_sessions() == []
    assert layout.get_tasks() == ["rest"]
    assert layout.get_runs() == [1, 2]

    epi_file = os.path.join(bids_dir.name, "sub-01", "fmap", "sub-01_dir-AP_epi.json")
    data = load_json(epi_file)

    assert os.path.exists(epi_file)
    assert data["IntendedFor"] == ["bids::" + os.path.join("sub-01",
                                                           "dwi",
                                                           "sub-01_dwi.nii.gz"),
                                   "bids::" + os.path.join("sub-01",
                                                           "anat",
                                                           "sub-01_T1w.nii")]

    func_task = os.path.join(bids_dir.name, "sub-01",
                             "func",
                             "sub-01_task-rest_acq-highres_bold.json")
    data = load_json(func_task)

    assert os.path.exists(func_task)
    assert data['TaskName'] == "rest"


def test_dcm2bids_complex():
    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR, "config_test_complex.json"),
                      bids_dir.name)
    app.run()

    layout = BIDSLayout(bids_dir.name, validate=False)

    assert layout.get_subjects() == ["01"]
    assert layout.get_sessions() == []
    assert layout.get_runs() == [1, 2, 3]

    fmap_file_1 = os.path.join(bids_dir.name,
                               "sub-01",
                               "fmap",
                               "sub-01_run-01_fmap.json")
    fmap_file_2 = os.path.join(bids_dir.name,
                               "sub-01",
                               "fmap",
                               "sub-01_run-02_fmap.json")
    fmap_file_3 = os.path.join(bids_dir.name,
                               "sub-01",
                               "fmap",
                               "sub-01_run-03_fmap.json")
    assert os.path.exists(fmap_file_1)
    assert os.path.exists(fmap_file_2)
    assert os.path.exists(fmap_file_3)

    localizer_file_1 = os.path.join(bids_dir.name,
                                    "sub-01",
                                    "localizer",
                                    "sub-01_run-01_localizer.json")
    localizer_file_2 = os.path.join(bids_dir.name,
                                    "sub-01",
                                    "localizer",
                                    "sub-01_run-02_localizer.json")
    assert os.path.exists(localizer_file_1)
    assert os.path.exists(localizer_file_2)

    mprage = os.path.join(bids_dir.name, "sub-01", "anat", "sub-01_T1w.json")
    assert not os.path.exists(mprage)


def test_dcm2bids_dup():
    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR, "config_test_dup.json"),
                      bids_dir.name)
    app.run()

    layout = BIDSLayout(bids_dir.name,
                        validate=False)

    original_01_localizer = os.path.join(TEST_DATA_DIR,
                                         "sidecars",
                                         "001_localizer_20100603125600_i00001.json")

    original_02_localizer = os.path.join(TEST_DATA_DIR,
                                         "sidecars",
                                         "001_localizer_20100603125600_i00002.json")

    original_03_localizer = os.path.join(TEST_DATA_DIR,
                                         "sidecars",
                                         "001_localizer_20100603125600_i00003.json")

    # Input localizer is lowercase (json)
    json_localizer = layout.get(subject="01",
                                extension="json",
                                suffix="localizer")
    # dup 01
    assert compare_json(original_01_localizer,
                        json_localizer[0].path)

    # dup 02
    assert compare_json(original_03_localizer,
                        json_localizer[1].path)

    # not dup
    assert compare_json(original_02_localizer,
                        json_localizer[2])


def test_dcm2bids_float():
    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR, "config_test_float.json"),
                      bids_dir.name)
    app.run()
    layout = BIDSLayout(bids_dir.name,
                        validate=False)

    assert layout.get_runs() == [1, 2, 3]

    original_fmap = os.path.join(TEST_DATA_DIR,
                                 "sidecars",
                                 "010_gre_field_mapping_20100603125600_e1.json")

    # Input localizer is lowercase (json)
    json_fmap = layout.get(subject="01",
                           extension="json",
                           suffix="fmap")

    assert compare_json(original_fmap,
                        json_fmap[0].path)

    localizer_file_1 = os.path.join(bids_dir.name,
                                    "sub-01",
                                    "localizer",
                                    "sub-01_run-01_localizer.json")
    localizer_file_2 = os.path.join(bids_dir.name,
                                    "sub-01",
                                    "localizer",
                                    "sub-01_run-02_localizer.json")
    localizer_file_3 = os.path.join(bids_dir.name,
                                    "sub-01",
                                    "localizer",
                                    "sub-01_run-03_localizer.json")
    fmap_file = os.path.join(bids_dir.name,
                             "sub-01",
                             "fmap",
                             "sub-01_echo-1_fmap.json")
    t1w_file = os.path.join(bids_dir.name,
                            "sub-01",
                            "anat",
                            "sub-01_T1w.json")

    assert os.path.exists(localizer_file_1)
    assert os.path.exists(localizer_file_2)
    assert os.path.exists(localizer_file_3)

    assert os.path.exists(fmap_file)
    assert os.path.exists(t1w_file)


def test_dcm2bids_sidecar():
    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01_ses-dev")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR, "config_test_sidecar.json"),
                      bids_dir.name,
                      session="dev")
    app.run()

    # existing field
    data = load_json(os.path.join(bids_dir.name,
                                  "sub-01",
                                  "ses-dev",
                                  "localizer",
                                  "sub-01_ses-dev_run-01_localizer.json"))
    assert data["ProcedureStepDescription"] == "Modified by dcm2bids"

    # new field
    data = load_json(os.path.join(bids_dir.name,
                                  "sub-01",
                                  "ses-dev",
                                  "anat",
                                  "sub-01_ses-dev_T1w.json"))
    assert data["new_field"] == "new value"
    assert 'AcquisitionNumber' not in list(data.keys())

    # boolean value
    data = load_json(os.path.join(bids_dir.name,
                                  "sub-01",
                                  "ses-dev",
                                  "fmap",
                                  "sub-01_ses-dev_echo-492_fmap.json"))
    assert data["MTState"]

    # boolean value if input as a string
    data = load_json(os.path.join(bids_dir.name,
                                  "sub-01",
                                  "ses-dev",
                                  "fmap",
                                  "sub-01_ses-dev_echo-738_fmap.json"))
    assert data["MTState"] == "false"

    # list with > 1 items
    data = load_json(os.path.join(bids_dir.name,
                                  "sub-01",
                                  "ses-dev",
                                  "dwi",
                                  "sub-01_ses-dev_desc-fa01_dwi.json"))
    assert data["IntendedFor"] == ["bids::" + os.path.join("sub-01",
                                                           "ses-dev",
                                                           "dwi",
                                                           "sub-01_ses-dev_dwi.nii.gz"),
                                   "bids::" + os.path.join("sub-01",
                                                           "ses-dev",
                                                           "anat",
                                                           "sub-01_ses-dev_T1w.nii")]
    assert data["Sources"] == ["bids::" + os.path.join("sub-01",
                                                       "ses-dev",
                                                       "anat",
                                                       "sub-01_ses-dev_T1w.nii"),
                               "bids::" + os.path.join("sub-01",
                                                       "ses-dev",
                                                       "dwi",
                                                       "sub-01_ses-dev_dwi.nii.gz")]

    # list with 1 item
    data = load_json(os.path.join(bids_dir.name,
                                  "sub-01",
                                  "ses-dev",
                                  "dwi",
                                  "sub-01_ses-dev_desc-trace_dwi.json"))
    assert data["IntendedFor"] == "bids::" + os.path.join("sub-01",
                                                          "ses-dev",
                                                          "dwi",
                                                          "sub-01_ses-dev_dwi.nii.gz")
    assert data["Sources"] == "bids::" + os.path.join("sub-01",
                                                      "ses-dev",
                                                      "anat",
                                                      "sub-01_ses-dev_T1w.nii")


def test_dcm2bids_multiple_intendedFor():
    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR,
                                   "config_test_multiple_intendedfor.json"),
                      bids_dir.name,
                      auto_extract_entities=True)
    app.run()

    epi_file = os.path.join(bids_dir.name, "sub-01", "fmap", "sub-01_fmap.json")
    data = load_json(epi_file)

    assert os.path.exists(epi_file)
    assert data["IntendedFor"] == ["bids::" + os.path.join("sub-01",
                                                           "localizer",
                                                           "sub-01_run-01_localizer.nii"),
                                   "bids::" + os.path.join("sub-01",
                                                           "localizer",
                                                           "sub-01_run-02_localizer.nii"),
                                   "bids::" + os.path.join("sub-01",
                                                           "localizer",
                                                           "sub-01_run-03_localizer.nii"),
                                   "bids::" + os.path.join("sub-01",
                                                           "anat",
                                                           "sub-01_T1w.nii")]


def test_dcm2bids_no_reorder_entities():
    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR, "config_test_no_reorder.json"),
                      bids_dir.name,
                      do_not_reorder_entities=True,
                      auto_extract_entities=False)
    app.run()

    # existing field
    func_json = os.path.join(bids_dir.name, "sub-01",
                             "func",
                             "sub-01_acq-highres_task-rest_bold.json")
    assert os.path.exists(func_json)


def test_dcm2bids_multiple_intendedFor_uri():
    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR,
                                   "config_test_multiple_intendedfor_uri_relative.json"),
                      bids_dir.name,
                      auto_extract_entities=True)
    app.run()

    epi_file = os.path.join(bids_dir.name, "sub-01", "fmap", "sub-01_fmap.json")
    data = load_json(epi_file)

    assert os.path.exists(epi_file)
    assert data["IntendedFor"] == [os.path.join("localizer",
                                                "sub-01_run-01_localizer.nii"),
                                   os.path.join("localizer",
                                                "sub-01_run-02_localizer.nii"),
                                   os.path.join("localizer",
                                                "sub-01_run-03_localizer.nii"),
                                   os.path.join("anat",
                                                "sub-01_T1w.nii")]


def test_dcm2bids_key_absent():
    # Validate case_sensitive false
    bids_dir = TemporaryDirectory()

    tmp_sub_dir = os.path.join(bids_dir.name, DEFAULT.tmp_dir_name, "sub-01")
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmp_sub_dir)

    app = Dcm2BidsGen(TEST_DATA_DIR, "01",
                      os.path.join(TEST_DATA_DIR,
                                   "config_test_key_absent.json"),
                      bids_dir.name)
    app.run()
    epi_file = os.path.join(bids_dir.name, "sub-01", "fmap", "sub-01_fmap.json")
    data = load_json(epi_file)
    assert os.path.exists(epi_file)
    assert data["SeriesNumber"] == 11
