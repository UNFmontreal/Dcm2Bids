# -*- coding: utf-8 -*-


import json
from glob import glob
import os
import pytest
from dcm2bids.sidecar import Sidecar


@pytest.fixture
def sidecarFiles():
    dataDir = os.path.join(os.path.dirname(__file__), "data", "sidecars")
    return glob(os.path.join(dataDir, "*.json"))


def test_sidecar_lt(sidecarFiles):

    sidecarsDcm2bids = sorted([Sidecar(_) for _ in sidecarFiles])
    sidecarsExpectedOnlyFilename = [Sidecar(_) for _ in sorted(sidecarFiles)]

    # 001_localizer_20100603125600_i00001.json
    # 001_localizer_20100603125600_i00003.json
    assert sidecarsDcm2bids[0] < sidecarsDcm2bids[1]

    # 003_MPRAGE_20100603125600.json
    # 001_localizer_20100603125600_i00002.json
    assert sidecarsDcm2bids[4] > sidecarsDcm2bids[2]

    # 001_localizer_20100603125600_i00002.json
    assert sidecarsDcm2bids[2] == sidecarsExpectedOnlyFilename[1]


def test_sidecar_lt_compares_acquisition_time_numerically(tmp_path):
    early_file = tmp_path / "early.json"
    late_file = tmp_path / "late.json"

    with early_file.open("w") as f:
        json.dump({"SeriesNumber": 1, "AcquisitionTime": "08:39:6.332500"}, f)

    with late_file.open("w") as f:
        json.dump({"SeriesNumber": 1, "AcquisitionTime": "08:39:12.180000"}, f)

    early = Sidecar(str(early_file))
    late = Sidecar(str(late_file))

    assert early < late
    assert sorted([late, early]) == [early, late]
