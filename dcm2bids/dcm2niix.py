# -*- coding: utf-8 -*-


import glob
import os
from subprocess import call
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
            print("")
            print("Old dcm2niix output found")
            print("Cleaning the old dcm2niix output and rerun it because --forceDcm2niix")
            print("")
            clean(self.outputDir)
            self.execute()

        elif oldOutput:
            print("")
            print("Old dcm2niix output found")
            print("Use --forceDcm2niix to rerun the conversion")

        else:
            clean(self.outputDir)
            self.execute()

        self.sidecars = glob.glob(os.path.join(self.outputDir, "*.json"))
        self.sidecars.sort()
        return 0


    def execute(self):
        for directory in self.dicomDir:
            commandStr = "dcm2niix {} -o {} {}"
            command = commandStr.format(self.options, self.outputDir, directory)
            call(command, shell=True)

