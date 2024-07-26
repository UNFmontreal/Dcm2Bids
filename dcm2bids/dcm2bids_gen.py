# -*- coding: utf-8 -*-

"""
Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure
"""

import logging
import os
from pathlib import Path
from glob import glob
import shutil

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
        force_dcm2bids (boolean): Forces a cleaning of a previous execution of
                                 dcm2bids
        log_level (str): logging level
    """

    def __init__(
        self,
        dicom_dir,
        participant,
        config,
        output_dir=DEFAULT.output_dir,
        bids_validate=DEFAULT.bids_validate,
        auto_extract_entities=DEFAULT.auto_extract_entities,
        do_not_reorder_entities = DEFAULT.do_not_reorder_entities,
        session=DEFAULT.session,
        clobber=DEFAULT.clobber,
        force_dcm2bids=DEFAULT.force_dcm2bids,
        skip_dcm2niix=DEFAULT.skip_dcm2niix,
        log_level=DEFAULT.logLevel,
        **_
    ):
        self._dicom_dirs = []
        self.dicom_dirs = dicom_dir
        self.bids_dir = valid_path(output_dir, type="folder")
        self.config = load_json(valid_path(config, type="file"))
        self.participant = Participant(participant, session)
        self.clobber = clobber
        self.bids_validate = bids_validate
        self.auto_extract_entities = auto_extract_entities
        self.do_not_reorder_entities = do_not_reorder_entities
        self.force_dcm2bids = force_dcm2bids
        self.skip_dcm2niix = skip_dcm2niix
        self.logLevel = log_level
        self.logger = logging.getLogger(__name__)

        if self.auto_extract_entities and self.do_not_reorder_entities:
            raise ValueError("Auto extract entities is set to True and "
                              "do not reorder entities is set to True. "
                              "Please choose only one option.")

    @property
    def dicom_dirs(self):
        """List of DICOMs directories"""
        return self._dicom_dirs

    @dicom_dirs.setter
    def dicom_dirs(self, value):

        dicom_dirs = value if isinstance(value, list) else [value]

        valid_dirs = [valid_path(_dir, "folder") for _dir in dicom_dirs]

        self._dicom_dirs = valid_dirs

    def run(self):
        """Run dcm2bids"""
        dcm2niix = Dcm2niixGen(
            self.dicom_dirs,
            self.bids_dir,
            self.participant,
            self.skip_dcm2niix,
            self.config.get("dcm2niixOptions", DEFAULT.dcm2niixOptions),
        )

        dcm2niix.run(self.force_dcm2bids)

        sidecars = []
        for filename in dcm2niix.sidecarFiles:
            sidecars.append(
                Sidecar(filename, self.config.get("compKeys", DEFAULT.compKeys))
            )

        sidecars = sorted(sidecars)

        parser = SidecarPairing(
            sidecars,
            self.config["descriptions"],
            self.config.get("extractors", {}),
            self.auto_extract_entities,
            self.do_not_reorder_entities,
            self.config.get("search_method", DEFAULT.search_method),
            self.config.get("case_sensitive", DEFAULT.case_sensitive),
            self.config.get("dup_method", DEFAULT.dup_method),
            self.config.get("post_op",  DEFAULT.post_op),
            self.config.get("bids_uri",  DEFAULT.bids_uri)
        )
        parser.build_graph()
        parser.build_acquisitions(self.participant)
        parser.find_runs()

        output_dir = os.path.join(self.bids_dir, self.participant.directory)
        if parser.acquisitions:
            self.logger.info("Moving acquisitions into BIDS "
                             f"folder \"{output_dir}\".\n")
        else:
            self.logger.warning("No pairing was found. "
                                f"BIDS folder \"{output_dir}\" won't be created. "
                                "Check your config file.\n".upper())

        idList = {}
        for acq in parser.acquisitions:
            idList = self.move(acq, idList, parser.post_op)

        if self.bids_validate:
            try:
                self.logger.info("BIDS VALIDATION")
                bids_version = run_shell_command(['bids-validator', '-v'], False)
                self.logger.info(f"Use bids-validator version: {bids_version.decode()[:-1]}")
                bids_report = run_shell_command(['bids-validator', self.bids_dir])
                self.logger.info("Report from bids-validator")
                self.logger.info(bids_report.decode())
            except Exception:
                self.logger.error("The bids-validator does not seem to work properly. "
                                  "The bids-validator may not be installed on your "
                                  "computer. Please check: "
                                  "https://github.com/bids-standard/bids-validator.")

    def move(self, acq, idList, post_op):
        """Move an acquisition to BIDS format"""
        for srcFile in sorted(glob(f"{acq.srcRoot}.*"), reverse=True):
            ext = Path(srcFile).suffixes
            ext = [curr_ext for curr_ext in ext if curr_ext in ['.nii', '.gz',
                                                                '.json',
                                                                '.bval', '.bvec']]

            dstFile = (self.bids_dir / acq.dstRoot).with_suffix("".join(ext))

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
                if acq.id in idList:
                    idList[acq.id].append(os.path.join(acq.participant.name,
                                                       acq.dstId + "".join(ext)))
                else:
                    idList[acq.id] = [os.path.join(acq.participant.name,
                                                   acq.dstId + "".join(ext))]

                for curr_post_op in post_op:
                    if acq.datatype in curr_post_op['datatype'] or 'any' in curr_post_op['datatype']:
                        if acq.suffix in curr_post_op['suffix'] or '_any' in curr_post_op['suffix']:
                            cmd = curr_post_op['cmd'].replace('src_file', str(srcFile))

                            # If custom entities it means that the user
                            # wants to have both versions
                            # before and after post_op
                            if 'custom_entities' in curr_post_op:
                                acq.setExtraDstFile(curr_post_op["custom_entities"])
                                extraDstFile = self.bids_dir / acq.extraDstFile
                                # Copy json file with this new set of custom entities.
                                shutil.copy(
                                    str(srcFile).replace("".join(ext), ".json"),
                                    f"{str(extraDstFile)}.json",
                                )
                                cmd = cmd.replace('dst_file',
                                                  str(extraDstFile) + ''.join(ext))
                            else:
                                cmd = cmd.replace('dst_file', str(dstFile))

                            try:
                                std_out = run_shell_command(cmd.split())
                                self.logger.debug(f"Log from: {cmd}")
                                self.logger.debug(std_out.decode())
                                self.logger.info("")
                                continue
                            except Exception:
                                self.logger.error(
                                  f"The command post_op: \"{cmd}\" "
                                  "does not seem to work properly. "
                                  "Check if it is installed on your "
                                  "computer.\n")

            if ".json" in ext:
                data = acq.dstSidecarData(idList)
                save_json(dstFile, data)
                os.remove(srcFile)

            # just move
            elif not os.path.exists(dstFile):
                os.rename(srcFile, dstFile)

        return idList
