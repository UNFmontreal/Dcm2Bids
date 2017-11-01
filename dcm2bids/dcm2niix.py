# -*- coding: utf-8 -*-


import glob
import logging
import os
import shlex
import subprocess
from .utils import clean


class Dcm2niix(object):
    """
    """

    def __init__(self, dicom_dir, bidsDir,
            participant=None, output="dcm2niix-example"):
        self.dicomDir = dicom_dir
        self.bidsDir = bidsDir
        self.participant = participant
        self.output = output
        self.options = "-b y -ba y -z y -f '%3s_%f_%p_%t'"
        self.sidecars = []
        self.logger = logging.getLogger("dcm2bids")


    @property
    def outputDir(self):
        if self.participant is None:
            return os.path.join(self.bidsDir, "tmp_dcm2bids", self.output)
        else:
            return os.path.join(
                    self.bidsDir, "tmp_dcm2bids", self.participant.prefix)


    def run(self, forceRun=False):
        try:
            oldOutput = os.listdir(self.outputDir) != []
        except:
            oldOutput = False

        if oldOutput and forceRun:
            self.logger.info("Old dcm2niix output found")
            self.logger.info("Cleaning the old dcm2niix output and rerun it because --forceDcm2niix")
            self.logger.info("")
            clean(self.outputDir)
            self.execute()

        elif oldOutput:
            self.logger.info("Old dcm2niix output found")
            self.logger.info("Use --forceDcm2niix to rerun the conversion")

        else:
            clean(self.outputDir)
            self.execute()

        self.sidecars = glob.glob(os.path.join(self.outputDir, "*.json"))
        self.sidecars.sort()
        return 0


    def _run_shell_command(self, commandLine):
        cmd = shlex.split(commandLine)
        self.logger.info("subprocess: {}".format(commandLine))

        try:
            process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, _ = process.communicate()

            try:
                self.logger.info("\n" + output.decode("utf-8"))
            except:
                self.logger.info(output)

        except OSError as exception:
            self.logger.error("Exception: {}".format(exeception))
            self.logger.info("subprocess failed")


    def execute(self):
        self.logger.info("--- running dcm2niix ---")
        for directory in self.dicomDir:
            commandStr = "dcm2niix {} -o {} {}"
            self._run_shell_command(
                    commandStr.format(self.options, self.outputDir, directory))

