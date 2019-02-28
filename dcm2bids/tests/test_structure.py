# -*- coding: utf-8 -*-


import pytest
from dcm2bids.structure import Participant, Acquisition
from os.path import join as opj


@pytest.mark.parametrize("srcRoot,extension,expected", [
    ("0006_MPRAGE", "json", "0006_MPRAGE.json"),
    ("0006_MPRAGE", ".json", "0006_MPRAGE.json"),
    ("0006_MPRAGE", "nii.gz", "0006_MPRAGE.nii.gz"),
    ("0006_MPRAGE", ".nii.gz", "0006_MPRAGE.nii.gz"),
])
def test_acquisition_get_src_path(srcRoot, extension, expected):
    participant = Participant("ABC")
    acquisition = Acquisition(srcRoot, participant, "anat", "T1w")
    assert acquisition.get_src_path(extension) == expected


@pytest.mark.parametrize("name,session,modality,custom,extension,expected", [
    ("AB", "", "T1w", "", "json",
        opj("sub-AB", "anat", "sub-AB_T1w.json")),
    ("sub-AB", "  ", "_T1w", "run-03", ".json",
        opj("sub-AB", "anat", "sub-AB_run-03_T1w.json")),
    ("sub-AB", "01", "_T1w", "  ", "nii.gz",
        opj("sub-AB", "ses-01", "anat", "sub-AB_ses-01_T1w.nii.gz")),
    ("sub-AB", "ses-01", "_T1w", "_run-03", ".nii.gz",
        opj("sub-AB", "ses-01", "anat", "sub-AB_ses-01_run-03_T1w.nii.gz")),
])
def test_acquisition_get_dst_path(name, session, modality, custom, extension,
                                  expected):
    participant = Participant(name, session)
    acquisition = Acquisition("srcRoot", participant, "anat", modality, custom)
    assert acquisition.get_dst_path(extension) == expected

