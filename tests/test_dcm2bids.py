# -*- coding: utf-8 -*-


import os
import shutil
from tempfile import TemporaryDirectory

from bids import BIDSLayout
from dcm2bids import Dcm2bids
from dcm2bids.utils import DEFAULT, load_json


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def validate_default_dcm2bids(bidsDir, tmpSubDir):
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

    # RERUN dcm2bids
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


def validate_dup_dcm2bids(bidsDir, tmpSubDir):
    # Validate duplicateMethod: dup
    shutil.rmtree(tmpSubDir)
    shutil.copytree(os.path.join(TEST_DATA_DIR, "sidecars"), tmpSubDir)

    app = Dcm2bids(
        [TEST_DATA_DIR],
        "01",
        os.path.join(TEST_DATA_DIR, "config_test_dup_option.json"),
        bidsDir.name,
    )
    app.run()

    dupLocalizerFile = os.path.join(bidsDir.name,
                                    "sub-01",
                                    "localizer",
                                    "sub-01_localizer_dup-01.json")

    assert os.path.exists(dupLocalizerFile)


def main():
    bidsDir = TemporaryDirectory()
    tmpSubDir = os.path.join(bidsDir.name, DEFAULT.tmpDirName, "sub-01")
    validate_default_dcm2bids(bidsDir, tmpSubDir)
    validate_dup_dcm2bids(bidsDir, tmpSubDir)

    if os.name != 'nt':
        bidsDir.cleanup()


if __name__ == '__main__':
    main()
