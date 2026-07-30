# -*- coding: utf-8 -*-

from pathlib import Path
from unittest.mock import MagicMock, patch
from tempfile import TemporaryDirectory

from dcm2bids.utils.utils import DEFAULT
from dcm2bids.cli.dcm2bids_helper import main


def test_help_option(script_runner):
    ret = script_runner.run(['dcm2bids_helper', '--help'])
    assert ret.success


def test_helper_default_output_dir(monkeypatch):
    i_tmpDir = TemporaryDirectory()

    mock_logger = MagicMock()
    expected_default_out_dir = Path(DEFAULT.output_dir) / DEFAULT.tmp_dir_name / DEFAULT.helper_dir
    mock_gen = MagicMock()
    mock_gen.run.return_value = "HELPER_RETURN_DEFAULT"

    with patch("dcm2bids.cli.dcm2bids_helper.Dcm2niixGen") as MockGen, \
         patch("dcm2bids.cli.dcm2bids_helper.dcm2niix_version", return_value="1.0"), \
         patch("dcm2bids.cli.dcm2bids_helper.check_latest", return_value=None), \
         patch("dcm2bids.cli.dcm2bids_helper.setup_logging", return_value=None), \
         patch("dcm2bids.cli.dcm2bids_helper.logging.getLogger", return_value=mock_logger):

        MockGen.return_value = mock_gen

        monkeypatch.setattr(
            "sys.argv",
            [
                "dcm2bids_helper",
                "-d", i_tmpDir.name,
                "--force",
                "-l", "ERROR",
            ],
        )

        result = main()

    assert result == "HELPER_RETURN_DEFAULT"
    assert MockGen.call_args_list[0].kwargs == {
        "dicom_dirs": [i_tmpDir.name],
        "bids_dir": expected_default_out_dir,
        "helper": True,
    }
    mock_gen.run.assert_called_once_with(force=True)
    mock_logger.info.assert_any_call(f"Helper files in: {expected_default_out_dir}\n")
    i_tmpDir.cleanup()


def test_helper_custom_output_dir_and_nested(monkeypatch):
    i_tmpDir = TemporaryDirectory()
    o_tmpDir = TemporaryDirectory()

    mock_logger = MagicMock()
    mock_gen = MagicMock()
    mock_gen.run.return_value = "HELPER_RETURN_NESTED"

    expected_nested_out_dir = Path(o_tmpDir.name) / DEFAULT.tmp_dir_name / DEFAULT.helper_dir / "nested"

    with patch("dcm2bids.cli.dcm2bids_helper.Dcm2niixGen") as MockGen, \
         patch("dcm2bids.cli.dcm2bids_helper.dcm2niix_version", return_value="1.0"), \
         patch("dcm2bids.cli.dcm2bids_helper.check_latest", return_value=None), \
         patch("dcm2bids.cli.dcm2bids_helper.setup_logging", return_value=None), \
         patch("dcm2bids.cli.dcm2bids_helper.logging.getLogger", return_value=mock_logger):

        MockGen.return_value = mock_gen

        monkeypatch.setattr(
            "sys.argv",
            [
                "dcm2bids_helper",
                "-d", i_tmpDir.name,
                "-o", o_tmpDir.name,
                "-n", "nested",
                "--force",
                "-l", "ERROR",
            ],
        )

        result = main()

    assert result == "HELPER_RETURN_NESTED"
    assert MockGen.call_args_list[0].kwargs == {
        "dicom_dirs": [i_tmpDir.name],
        "bids_dir": expected_nested_out_dir,
        "helper": True,
    }
    mock_gen.run.assert_called_once_with(force=True)
    mock_logger.info.assert_any_call(f"Helper files in: {expected_nested_out_dir}\n")
    i_tmpDir.cleanup()
    o_tmpDir.cleanup()
