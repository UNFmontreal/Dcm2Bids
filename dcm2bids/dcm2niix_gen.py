# -*- coding: utf-8 -*-

"""Dcm2niix class"""

import logging
import os
import shlex
import shutil
from glob import glob

from dcm2bids.utils.utils import DEFAULT, run_shell_command


class Dcm2niixGen(object):
    """ Object to handle dcm2niix execution

    Args:
        dicom_dirs (list): A list of folder with dicoms to convert
        bids_dir (str): A path to the root BIDS directory
        participant: Optional Participant object
        options (str): Optional arguments for dcm2niix

    Properties:
        sidecars (list): A list of sidecar path created by dcm2niix
    """

    def __init__(
        self,
        dicom_dirs,
        bids_dir,
        participant=None,
        options=DEFAULT.dcm2niixOptions,
        helper=False
    ):
        self.logger = logging.getLogger(__name__)
        self.sidecarsFiles = []
        self.dicom_dirs = dicom_dirs
        self.bids_dir = bids_dir
        self.participant = participant
        self.options = options
        self.helper = helper

    @property
    def output_dir(self):
        """
        Returns:
            A directory to save all the output files of dcm2niix
        """
        tmpDir = self.participant.prefix if self.participant else DEFAULT.helper_dir
        tmpDir = self.bids_dir / DEFAULT.tmp_dir_name / tmpDir
        if self.helper:
            tmpDir = self.bids_dir
        return tmpDir

    def run(self, force=False, helper=False):
        """ Run dcm2niix if necessary

        Args:
            force (boolean): Forces a cleaning of a previous execution of
                             dcm2niix

        Sets:
            sidecarsFiles (list): A list of sidecar path created by dcm2niix
        """
        try:
            oldOutput = os.listdir(self.output_dir) != []
        except Exception:
            oldOutput = False

        if oldOutput and force:
            self.logger.warning("Previous dcm2niix directory output found:")
            self.logger.warning(self.output_dir)
            self.logger.warning("'force' argument is set to True")
            self.logger.warning("Cleaning the previous directory and running dcm2niix")

            shutil.rmtree(self.output_dir, ignore_errors=True)

            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

            self.execute()

        elif oldOutput:
            self.logger.warning("Previous dcm2niix directory output found:")
            self.logger.warning(self.output_dir)
            self.logger.warning("Use --force_dcm2niix to rerun dcm2niix\n")

        else:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

            self.execute()

        self.sidecarFiles = glob(os.path.join(self.output_dir, "*.json"))

    def execute(self):
        """ Execute dcm2niix for each directory in dicom_dirs
        """
        for dicomDir in self.dicom_dirs:
            cmd = ['dcm2niix', *shlex.split(self.options),
                   '-o', self.output_dir, dicomDir]
            output = run_shell_command(cmd)

            try:
                output = output.decode()
            except Exception:
                pass

            self.logger.debug(f"\n{output}")
            self.logger.info("Check log file for dcm2niix output\n")
