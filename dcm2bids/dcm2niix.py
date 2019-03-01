# -*- coding: utf-8 -*-


import glob
import logging
import os
from .utils import clean, run_shell_command


class Dcm2niix(object):
    """ Object to handle dcm2niix execution

    Args:
        dicomDirs (list): A list of folder with dicoms to convert
        bidsDir (str): A path to the root BIDS directory
        participant: Optional Participant object
        options (str): Optional arguments for dcm2niix

    Properties:
        sidecars (list): A list of sidecar path created by dcm2niix
    """

    def __init__(self, dicomDirs, bidsDir, participant=None,
                 options="-b y -ba y -z y -f '%3s_%f_%p_%t'"):
        self._sidecars = []

        self.dicomDirs = dicomDir
        self.bidsDir = bidsDir
        self.participant = participant
        self.options = options


    @property
    def sidecars(self):
        """
        Returns:
            sidecars (list): A list of sidecar path created by dcm2niix
        """
        return self._sidecars


    @property
    def outputDir(self):
        """
        Returns:
            A directory to save all the output files of dcm2niix
        """
        if self.participant:
            tmpDir = self.participant.prefix
        else:
            tmpDir = "helper"
        return os.path.join(self.bidsDir, "tmp_dcm2bids", tmpDir)


    def run(self, forceRun=False):
        try:
            oldOutput = os.listdir(self.outputDir) != []
        except:
            oldOutput = False

        if oldOutput and forceRun:
            if self._logger:
                self.logger.info("Old dcm2niix output found")
                self.logger.info("Cleaning the old dcm2niix output and rerun it because --forceDcm2niix")
                self.logger.info("")
            clean(self.outputDir)
            self.execute()

        elif oldOutput:
            if self._logger:
                self.logger.info("Old dcm2niix output found")
                self.logger.info("Use --forceDcm2niix to rerun the conversion")

        else:
            clean(self.outputDir)
            self.execute()

        self.sidecars = glob.glob(os.path.join(self.outputDir, "*.json"))
        self.sidecars.sort()

        return os.EX_OK


    def execute(self):
        """ Execute dcm2niix for each directory in dicomDirs
        """
        self.version()
        for dicomDir in self.dicomDirs:
            commandTpl = "dcm2niix {} -o {} {}"
            cmd = commandTpl.format(self.options, self.outputDir, dicomDir)
            run_shell_command(cmd)


    @staticmethod
    def version():
        """
        Returns:
            A string of the version of dcm2niix install on the system
        """
        try:
            output = run_shell_command("dcm2niix").decode()
            output = output.split("\n")[0].split()
            version = output[output.index('version')+1]
            logging.info("Running dcm2niix version " + version)

        except FileNotFoundError:
            logging.error("dcm2niix does not appear to be installed")
            logging.error("See: https://github.com/rordenlab/dcm2niix")
            version = ""

        return version

