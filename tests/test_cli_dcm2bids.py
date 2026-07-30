# -*- coding: utf-8 -*-
import json
import sys
from unittest.mock import MagicMock, patch

import pytest

from dcm2bids.cli.dcm2bids import main, _build_arg_parser


def test_main_runs_success(tmp_path, monkeypatch):
    # prepare minimal inputs
    dicom_dir = tmp_path / "dicoms"
    dicom_dir.mkdir()

    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({}))

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    # patch external dependencies to keep the test focused and fast
    mock_logger = MagicMock()
    mock_gen = MagicMock()
    mock_gen.run.return_value = "APP_RETURN"

    with patch("dcm2bids.cli.dcm2bids.Dcm2BidsGen") as MockGen, \
         patch("dcm2bids.cli.dcm2bids.dcm2niix_version", return_value="1.0"), \
         patch("dcm2bids.cli.dcm2bids.check_latest", return_value=None), \
         patch("dcm2bids.cli.dcm2bids.setup_logging", return_value=None), \
         patch("dcm2bids.cli.dcm2bids.Participant") as MockParticipant, \
         patch("dcm2bids.cli.dcm2bids.logging.getLogger", return_value=mock_logger):

        MockGen.return_value = mock_gen
        # Participant should provide prefix, name and session attributes
        MockParticipant.return_value.prefix = "sub-01"
        MockParticipant.return_value.name = "01"
        MockParticipant.return_value.session = "ses-dev"

        monkeypatch.setattr(sys, "argv", [
            "dcm2bids", "-d", str(dicom_dir),
            "-p", "01",
            "-s", "dev",
            "-c", str(config_file),
            "-o", str(output_dir),
        ])

        result = main()

    assert result == "APP_RETURN"
    MockGen.assert_called_once()
    mock_logger.info.assert_any_call("session: ses-dev")


def test_parser_mutually_exclusive_flags_raise():
    parser = _build_arg_parser()
    # both flags cannot be provided at the same time
    with pytest.raises(SystemExit):
        parser.parse_args([
            "-d", "some_dir",
            "-p", "01",
            "-c", "config.json",
            "--auto_extract_entities",
            "--do_not_reorder_entities",
        ])


def test_version_flag_exits():
    parser = _build_arg_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--version"])


def test_main_propagates_run_exceptions(tmp_path, monkeypatch):
    dicom_dir = tmp_path / "dicoms"
    dicom_dir.mkdir()

    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({}))

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    # Dcm2BidsGen.run raises
    mock_gen = MagicMock()
    mock_gen.run.side_effect = RuntimeError("boom")

    with patch("dcm2bids.cli.dcm2bids.Dcm2BidsGen") as MockGen, \
         patch("dcm2bids.cli.dcm2bids.dcm2niix_version", return_value="1.0"), \
         patch("dcm2bids.cli.dcm2bids.check_latest", return_value=None), \
         patch("dcm2bids.cli.dcm2bids.setup_logging", return_value=None), \
         patch("dcm2bids.cli.dcm2bids.Participant") as MockParticipant:

        MockGen.return_value = mock_gen
        MockParticipant.return_value.prefix = "sub-01"
        MockParticipant.return_value.name = "01"
        MockParticipant.return_value.session = None

        monkeypatch.setattr(sys, "argv", [
            "dcm2bids", "-d", str(dicom_dir),
            "-p", "01",
            "-c", str(config_file),
            "-o", str(output_dir),
        ])

        with pytest.raises(RuntimeError):
            main()


def test_cli_flags_forwarded_to_Dcm2BidsGen(tmp_path, monkeypatch):
    dicom_dir = tmp_path / "dicoms"
    dicom_dir.mkdir()

    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({}))

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    with patch("dcm2bids.cli.dcm2bids.Dcm2BidsGen") as MockGen, \
         patch("dcm2bids.cli.dcm2bids.dcm2niix_version", return_value="1.0"), \
         patch("dcm2bids.cli.dcm2bids.check_latest", return_value=None), \
         patch("dcm2bids.cli.dcm2bids.setup_logging", return_value=None), \
         patch("dcm2bids.cli.dcm2bids.Participant") as MockParticipant:

        MockGen.return_value = MagicMock()
        MockParticipant.return_value.prefix = "sub-01"
        MockParticipant.return_value.name = "01"
        MockParticipant.return_value.session = None

        monkeypatch.setattr(sys, "argv", [
            "dcm2bids", "-d", str(dicom_dir),
            "-p", "01",
            "-c", str(config_file),
            "-o", str(output_dir),
            "--skip_dcm2niix",
            "--clobber",
            "--force_dcm2bids",
            "--auto_extract_entities",
        ])

        main()

        # ensure Dcm2BidsGen was called with CLI flags present in kwargs
        assert MockGen.call_count == 1
        call_args = MockGen.call_args[1]
        assert call_args.get("skip_dcm2niix") is True
        assert call_args.get("clobber") is True
        assert call_args.get("force_dcm2bids") is True
        assert call_args.get("auto_extract_entities") is True


