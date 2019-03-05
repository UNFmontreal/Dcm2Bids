# -*- coding: utf-8 -*-


import logging
import os
import shutil
from distutils.version import LooseVersion
from glob import glob
from .utils import DEFAULT, run_shell_command


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
            options=DEFAULT.options):
        self.logger = logging.getLogger(__name__)

        self.sidecarsFiles = []

        self.dicomDirs = dicomDir
        self.bidsDir = bidsDir
        self.participant = participant
        self.options = options


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
        return os.path.join(self.bidsDir, TMP_DIR_NAME, tmpDir)


    def run(self, force=False):
        """ Run dcm2niix if necessary

        Args:
            force (boolean): Forces a cleaning of a previous execution of
                             dcm2niix

        Sets:
            sidecarsFiles (list): A list of sidecar path created by dcm2niix
        """
        try:
            oldOutput = os.listdir(self.outputDir) != []
        except:
            oldOutput = False

        if oldOutput and forceRun:
            self.logger.warning("Previous dcm2niix directory output found:")
            self.logger.warning(self.outputDir)
            self.logger.warning("force argument is set to True")
            self.logger.warning("Cleaning the previous directory and run dcm2niix")

            shutil.rmtree(self.outputDir, ignore_errors=True)
            os.makedirs(self.outputDir, exist_ok=True)
            self.execute()

        elif oldOutput:
            self.logger.warning("Previous dcm2niix directory output found:")
            self.logger.warning(self.outputDir)
            self.logger.warning("Use --forceDcm2niix to rerun dcm2niix")

        else:
            os.makedirs(self.outputDir, exist_ok=True)
            self.execute()

        self.sidecarFiles = glob(os.path.join(self.outputDir, "*.json"))

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
            self.logger.info("Running dcm2niix version " + version)

            #check version
            if LooseVersion(version) < LooseVersion(DEFAULT.dcm2niixVersion):
                self.logger.warning(
                        "Inferior version than the tested version ({})".format(
                            DEFAULT.dcm2niixVersion))

        except OSError:
            self.logger.error("dcm2niix does not appear to be installed")
            self.logger.error("See: https://github.com/rordenlab/dcm2niix")
            version = ""

        return version

