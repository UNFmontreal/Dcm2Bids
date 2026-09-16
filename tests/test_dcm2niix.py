# -*- coding: utf-8 -*-


from glob import glob
from tempfile import TemporaryDirectory
import os
import pytest
from dcm2bids.dcm2niix_gen import Dcm2niixGen
from dcm2bids.utils.utils import DEFAULT


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.mark.skip(reason="Too long for now")
def test_dcm2niix_run():
    dicomDir = os.path.join(TEST_DATA_DIR, "sourcedata", "sub-01")
    # tmpBase = os.path.join(TEST_DATA_DIR, "tmp")
    # tmpDir = TemporaryDirectory(dir=tmpBase)
    tmpDir = TemporaryDirectory()

    app = Dcm2niixGen([dicomDir], tmpDir.name)
    app.run()

    helper_dir = os.path.join(tmpDir.name, DEFAULT.tmp_dir_name, DEFAULT.helper_dir, "*")
    ls = sorted(glob(helper_dir))
    firstMtime = [os.stat(_).st_mtime for _ in ls]
    assert "localizer_20100603125600" in ls[0]

    # files should not be change after a rerun
    app.run()
    secondMtime = [os.stat(_).st_mtime for _ in ls]
    assert firstMtime == secondMtime

    # files should be change after a forced rerun
    app.run(force=True)
    thirdMtime = [os.stat(_).st_mtime for _ in ls]
    assert firstMtime != thirdMtime

    if os.name != 'nt':
        tmpDir.cleanup()


def test_execute_handles_non_utf8_output(tmp_path, monkeypatch, caplog):
    """dcm2niix output that is not valid UTF-8 must not crash the warning check."""
    import dcm2bids.dcm2niix_gen as gen

    monkeypatch.setattr(gen, "run_shell_command", lambda cmd: b"\xff Warning: x")
    dicomDir = tmp_path / "dicom"
    dicomDir.mkdir()

    app = Dcm2niixGen([str(dicomDir)], tmp_path)
    with caplog.at_level("WARNING"):
        app.execute()

    assert "Warning: x" in caplog.text
