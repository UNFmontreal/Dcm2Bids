# -*- coding: utf-8 -*-

"""
Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure
"""

import logging
import os
from pathlib import Path
from glob import glob

from dcm2bids.dcm2niix_gen import Dcm2niixGen
from dcm2bids.sidecar import Sidecar, SidecarPairing
from dcm2bids.participant import Participant
from dcm2bids.utils.utils import DEFAULT, run_shell_command
from dcm2bids.utils.io import load_json, save_json, valid_path


class Dcm2BidsGen(object):
    """ Object to handle dcm2bids execution steps

    Args:
        dicom_dir (str or list): A list of folder with dicoms to convert
        participant (str): Label of your participant
        config (path): Path to a dcm2bids configuration file
        output_dir (path): Path to the BIDS base folder
        session (str): Optional label of a session
        clobber (boolean): Overwrite file if already in BIDS folder
        force_dcm2niix (boolean): Forces a cleaning of a previous execution of
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
        auto_extract_entities=DEFAULT.auto_extract_entities,
        session=DEFAULT.session,
        clobber=DEFAULT.clobber,
        force_dcm2niix=DEFAULT.force_dcm2niix,
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
        self.auto_extract_entities = auto_extract_entities
        self.force_dcm2niix = force_dcm2niix
        self.logLevel = log_level
        self.logger = logging.getLogger(__name__)

    @property
    def dicomDirs(self):
        """List of DICOMs directories"""
        return self._dicomDirs

    @dicomDirs.setter
    def dicomDirs(self, value):

        dicom_dirs = value if isinstance(value, list) else [value]

        valid_dirs = [valid_path(_dir, "folder") for _dir in dicom_dirs]

        self._dicomDirs = valid_dirs

    def run(self):
        """Run dcm2bids"""
        dcm2niix = Dcm2niixGen(
            self.dicomDirs,
            self.bidsDir,
            self.participant,
            self.config.get("dcm2niixOptions", DEFAULT.dcm2niixOptions),
        )

        dcm2niix.run(self.force_dcm2niix)

        sidecars = []
        for filename in dcm2niix.sidecarFiles:
            sidecars.append(
                Sidecar(filename, self.config.get("compKeys", DEFAULT.compKeys))
            )

        sidecars = sorted(sidecars)

        parser = SidecarPairing(
            sidecars,
            self.config["descriptions"],
            self.config.get("extractors", DEFAULT.extractors),
            self.auto_extract_entities,
            self.config.get("searchMethod", DEFAULT.searchMethod),
            self.config.get("caseSensitive", DEFAULT.caseSensitive)
        )
        parser.build_graph()
        parser.build_acquisitions(self.participant)
        parser.find_runs()

        self.logger.info("moving acquisitions into BIDS folder\n".upper())

        idList = {}
        for acq in parser.acquisitions:
            idList = self.move(acq, idList)

        if self.bids_validate:
            try:
                self.logger.info(f"Validate if {self.output_dir} is BIDS valid.")
                self.logger.info("Use bids-validator version: ")
                run_shell_command(['bids-validator', '-v'])
                run_shell_command(['bids-validator', self.bidsDir])
            except Exception:
                self.logger.error("The bids-validator does not seem to work properly. "
                                  "The bids-validator may not be installed on your "
                                  "computer. Please check: "
                                  "https://github.com/bids-standard/bids-validator.")

    def move(self, acquisition, idList):
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
                self.logger.info(f"'{dstFile}' already exists")

                if self.clobber:
                    self.logger.info("Overwriting because of --clobber option")

                else:
                    self.logger.info("Use --clobber option to overwrite")
                    continue

            # Populate idList
            if '.nii' in ext:
                if acquisition.id in idList:
                    idList[acquisition.id].append(acquisition.dstId + "".join(ext))
                else:
                    idList[acquisition.id] = [acquisition.dstId + "".join(ext)]

            if (self.config.get("defaceTpl") and acquisition.datatype == "anat" and ".nii" in ext):
                try:
                    os.remove(dstFile)
                except FileNotFoundError:
                    pass
                defaceTpl = self.config.get("defaceTpl")

                cmd = [w.replace('srcFile', srcFile) for w in defaceTpl]
                cmd = [w.replace('dstFile', dstFile) for w in defaceTpl]
                run_shell_command(cmd)

            elif ".json" in ext:
                data = acquisition.dstSidecarData(idList)
                save_json(dstFile, data)
                os.remove(srcFile)

            # just move
            else:
                os.rename(srcFile, dstFile)

        return idList
