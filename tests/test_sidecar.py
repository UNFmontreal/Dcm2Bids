# -*- coding: utf-8 -*-


import os
import pytest
from dcm2bids.sidecar import Sidecar
from glob import glob


@pytest.fixture
def sidecarFiles():
    dataDir = os.path.join(
            os.path.dirname(__file__), "data", "sidecars")
    return glob(os.path.join(dataDir, "*.json"))


def test_sidecar_lt(sidecarFiles):
    sidecarsDcm2bids = sorted([Sidecar(_) for _ in sidecarFiles])
    sidecarsExpected = [Sidecar(_) for _ in sorted(sidecarFiles)]

    assert sidecarsDcm2bids[0] < sidecarsDcm2bids[1]
    assert sidecarsDcm2bids[4] > sidecarsDcm2bids[2]
    assert sidecarsDcm2bids[3] == sidecarsExpected[3]

