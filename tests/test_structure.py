# -*- coding: utf-8 -*-


from os.path import join as opj
import pytest
from dcm2bids.structure import Participant, Acquisition


@pytest.mark.parametrize(
    "name,session,modality,custom,expected",
    [
        ("AB", "", "T1w", "", opj("sub-AB", "anat", "sub-AB_T1w")),
        ("sub-AB", "  ", "_T1w", "run-03", opj("sub-AB", "anat", "sub-AB_run-03_T1w")),
        (
            "sub-AB",
            "01",
            "_T1w",
            "  ",
            opj("sub-AB", "ses-01", "anat", "sub-AB_ses-01_T1w"),
        ),
        (
            "sub-AB",
            "ses-01",
            "T1w",
            "_run-03",
            opj("sub-AB", "ses-01", "anat", "sub-AB_ses-01_run-03_T1w"),
        ),
    ],
)
def test_acquisition_get_dst_path(name, session, modality, custom, expected):
    participant = Participant(name, session)
    acquisition = Acquisition(participant, "anat", modality, custom)
    assert acquisition.dstRoot == expected
