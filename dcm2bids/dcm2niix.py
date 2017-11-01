# -*- coding: utf-8 -*-


import glob
import logging
import os
from .utils import clean, run_shell_command


class Dcm2niix(object):
    """
    """

    def __init__(self, dicom_dir, bids_dir, participant=None):
        self.dicomDirs = dicom_dir
        self.bidsDir = bids_dir
        self.participant = participant
        self.options = "-b y -ba y -z y -f '%3s_%f_%p_%t'"
        self.sidecars = []
        self.logger = logging.getLogger("dcm2bids")

    @property
    def outputDir(self):
        if self.participant:
            tmpDir = self.participant.prefix
        else:
            tmpDir = "dcm2niix-example"
        return os.path.join(self.bidsDir, "tmp_dcm2bids", tmpDir)


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


    def execute(self):
        self.logger.info("--- running dcm2niix ---")
        for directory in self.dicomDirs:
            commandStr = "dcm2niix {} -o {} {}"
            cmd = commandStr.format(self.options, self.outputDir, directory)
            run_shell_command(cmd)
