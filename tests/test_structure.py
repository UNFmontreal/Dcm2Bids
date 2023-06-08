# -*- coding: utf-8 -*-


from os.path import join as opj
import pytest
from dcm2bids.participant import Participant
from dcm2bids.acquisition import Acquisition


@pytest.mark.parametrize(
    "name,session,modality,custom,expected",
    [
        ("AB", "", "T1w", "", opj("sub-AB", "anat", "sub-AB_T1w")),
        ("sub-AA", " ", "T1w_T2w", "new-test", opj("sub-AA", "anat", "sub-AA_new-test_T1w_T2w")),
        ("sub-AB", " ", "_T1w", "run-03", opj("sub-AB", "anat", "sub-AB_run-03_T1w")),
        ("sub-AB", "01", "_T1w", "  ", opj("sub-AB", "ses-01", "anat", "sub-AB_ses-01_T1w")),
        ("sub-AB", "ses-01", "T1w", "run-03", opj("sub-AB", "ses-01", "anat", "sub-AB_ses-01_run-03_T1w")),
        ("sub-AB", "ses-01", "T1w", "run-04_rec-test_ce-test", opj("sub-AB", "ses-01", "anat", "sub-AB_ses-01_ce-test_rec-test_run-04_T1w"))
    ],
)

def test_acquisition_get_dst_path(name, session, modality, custom, expected):
    participant = Participant(name, session)
    acquisition = Acquisition(participant, "anat", modality, customLabels=custom)
    acquisition.setDstFile()
    assert acquisition.dstRoot == expected

@pytest.mark.parametrize(
    "name_c,session_c,modality_c,custom_c",
    [
        ("AB", "", "_T1w", ""),
    ],
)

def test_comparison_acquisitions(name_c, session_c, modality_c, custom_c):
    participant = Participant(name_c, session_c)
    acquisition1 = Acquisition(participant, "anat", modality_c, customLabels=custom_c)
    acquisition2 = Acquisition(participant, "anat", modality_c, customLabels=custom_c)
    assert acquisition1 == acquisition2