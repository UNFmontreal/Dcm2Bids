# -*- coding: utf-8 -*-

"""
Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure
"""

import logging
import os
from pathlib import Path
import platform
import sys
from datetime import datetime
from glob import glob

from dcm2bids.dcm2niix_gen import Dcm2niixGen
from dcm2bids.utils.logger import setup_logging
from dcm2bids.sidecar import Sidecar, SidecarPairing
from dcm2bids.participant import Participant
from dcm2bids.utils.utils import DEFAULT, run_shell_command
from dcm2bids.utils.io import load_json, save_json, valid_path
from dcm2bids.utils.tools import check_latest, dcm2niix_version
from dcm2bids.version import __version__

class Dcm2BidsGen(object):
    """ Object to handle dcm2bids execution steps

    Args:
        dicom_dir (str or list): A list of folder with dicoms to convert
        participant (str): Label of your participant
        config (path): Path to a dcm2bids configuration file
        output_dir (path): Path to the BIDS base folder
        session (str): Optional label of a session
        clobber (boolean): Overwrite file if already in BIDS folder
        forceDcm2niix (boolean): Forces a cleaning of a previous execution of
                                 dcm2niix
        log_level (str): logging level
    """

    def __init__(
        self,
        dicom_dir,
        participant,
        config,
        output_dir=DEFAULT.outputDir,
        bids_validate=DEFAULT.bids_validate,
        session=DEFAULT.session,
        clobber=DEFAULT.clobber,
        forceDcm2niix=DEFAULT.forceDcm2niix,
        log_level=DEFAULT.logLevel,
        **_
    ):
        self._dicomDirs = []

        self.dicomDirs = dicom_dir
        self.bidsDir = valid_path(output_dir, type="folder")
        self.config = load_json(valid_path(config, type="file"))
        self.participant = Participant(participant, session)
        self.clobber = clobber
        self.bids_validate = bids_validate
        self.forceDcm2niix = forceDcm2niix
        self.logLevel = log_level

        # logging setup
        self.set_logger()

        self.logger.info("--- dcm2bids start ---")
        self.logger.info("OS:version: %s", platform.platform())
        self.logger.info("python:version: %s", sys.version.replace("\n", ""))
        self.logger.info("dcm2bids:version: %s", __version__)
        self.logger.info("dcm2niix:version: %s", dcm2niix_version())
        self.logger.info("participant: %s", self.participant.name)
        self.logger.info("session: %s", self.participant.session)
        self.logger.info("config: %s", os.path.realpath(config))
        self.logger.info("BIDS directory: %s", os.path.realpath(output_dir))
        self.logger.info("Validate BIDS: %s", self.bids_validate)


    @property
    def dicomDirs(self):
        """List of DICOMs directories"""
        return self._dicomDirs

    @dicomDirs.setter
    def dicomDirs(self, value):

        dicom_dirs = value if isinstance(value, list) else [value]

        valid_dirs = [valid_path(_dir, "folder") for _dir in dicom_dirs]

        self._dicomDirs = valid_dirs

    def set_logger(self):
        """ Set a basic logger"""
        logDir = self.bidsDir / DEFAULT.tmpDirName / "log"
        logFile = logDir / f"{self.participant.prefix}_{datetime.now().isoformat().replace(':', '')}.log"
        logDir.mkdir(parents=True, exist_ok=True)

        setup_logging(self.logLevel, logFile)
        self.logger = logging.getLogger(__name__)

    def run(self):
        """Run dcm2bids"""
        dcm2niix = Dcm2niixGen(
            self.dicomDirs,
            self.bidsDir,
            self.participant,
            self.config.get("dcm2niixOptions", DEFAULT.dcm2niixOptions),
        )

        check_latest()
        check_latest("dcm2niix")

        dcm2niix.run(self.forceDcm2niix)

        sidecars = []
        for filename in dcm2niix.sidecarFiles:
            sidecars.append(
                Sidecar(filename, self.config.get("compKeys", DEFAULT.compKeys))
            )

        sidecars = sorted(sidecars)

        parser = SidecarPairing(
            sidecars,
            self.config["descriptions"],
            self.config.get("searchMethod", DEFAULT.searchMethod),
            self.config.get("caseSensitive", DEFAULT.caseSensitive)
        )
        parser.build_graph()
        parser.build_acquisitions(self.participant)
        parser.find_runs()

        self.logger.info("moving acquisitions into BIDS folder")

        intendedForList = {}
        for acq in parser.acquisitions:
            acq.setDstFile()
            intendedForList = self.move(acq, intendedForList)

        if self.bids_validate:
            try:
                self.logger.info(f"Validate if { self.output_dir} is BIDS valid.")
                self.logger.info("Use bids-validator version: ")
                run_shell_command(['bids-validator', '-v'])
                run_shell_command(['bids-validator', self.bidsDir])
            except:
                self.logger.info("The bids-validator does not seem to work properly. "
                                 "The bids-validator may not been installed on your computer. "
                                 f"Please check: https://github.com/bids-standard/bids-validator#quickstart.")

    def move(self, acquisition, intendedForList):
        """Move an acquisition to BIDS format"""
        for srcFile in glob(acquisition.srcRoot + ".*"):
            ext = Path(srcFile).suffixes
            ext = [curr_ext for curr_ext in ext if curr_ext in ['.nii', '.gz',
                                                                '.json',
                                                                '.bval', '.bvec']]

            dstFile = (self.bidsDir / acquisition.dstRoot).with_suffix("".join(ext))

            dstFile.parent.mkdir(parents=True, exist_ok=True)

            # checking if destination file exists
            if dstFile.exists():
                self.logger.info("'%s' already exists", dstFile)

                if self.clobber:
                    self.logger.info("Overwriting because of --clobber option")

                else:
                    self.logger.info("Use --clobber option to overwrite")
                    continue

            # Populate intendedFor
            if '.nii' in ext:
                if acquisition.id in intendedForList:
                    intendedForList[acquisition.id].append(acquisition.dstIntendedFor + "".join(ext))
                else:
                    intendedForList[acquisition.id] = [acquisition.dstIntendedFor + "".join(ext)]

            # it's an anat nifti file and the user using a deface script
            if (self.config.get("defaceTpl") and acquisition.dataType == "anat" and ".nii" in ext):
                try:
                    os.remove(dstFile)
                except FileNotFoundError:
                    pass
                defaceTpl = self.config.get("defaceTpl")

                cmd = [w.replace('srcFile', srcFile) for w in defaceTpl]
                cmd = [w.replace('dstFile', dstFile) for w in defaceTpl]
                run_shell_command(cmd)

            elif ".json" in ext:
                data = acquisition.dstSidecarData(intendedForList)
                save_json(dstFile, data)
                os.remove(srcFile)

            # just move
            else:
                os.rename(srcFile, dstFile)

        return intendedForList