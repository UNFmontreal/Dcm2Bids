# -*- coding: utf-8 -*-


import glob
import os
from builtins import input
from .dcm2niix import Dcm2niix
from .sidecarparser import Sidecarparser
from .structure import Participant
from .utils import load_json, make_directory_tree, splitext_


class Dcm2bids(object):
    """
    """

    def __init__(self, dicom_dir, config, yes, participant, session=None):
        self.dicomDir = dicom_dir
        self.config = load_json(config)
        self.yes = yes
        self.participant = Participant(participant, session)


    @property
    def session(self):
        return self.participant.session

    @session.setter
    def session(self, value):
        self.participant.session = value


    def run(self):
        dcm2niix = Dcm2niix(self.dicomDir, self.participant)
        dcm2niix.run()
        parser = Sidecarparser(dcm2niix.sidecars, self.config["descriptions"])

        for acq in parser.acquisitions:
            state = self._move(acq)
            if state != 0: return state
        return 0


    def _move(self, acquisition):
        targetDir = os.path.join(
                os.getcwd(), self.participant.directory, acquisition.dataType)
        filename = "{}_{}".format(self.participant.prefix, acquisition.suffix)
        targetBase = os.path.join(targetDir, filename)

        targetNiigz = targetBase + ".nii.gz"
        if os.path.isfile(targetNiigz) and not self.yes:
            reply = self._ask(targetNiigz)
            if reply == "q":
                return 1
            elif reply == "a":
                self.yes = True

        make_directory_tree(targetDir)
        for f in glob.glob(acquisition.base + ".*"):
            _, ext = splitext_(f)
            os.rename(f, targetBase + ext)

        return 0


    def _ask(self, target):
        print("")
        print("'{}' already exists".format(os.path.basename(target)))
        print("This file will be erase and replace if you continue")
        while True:
            p = "Do you want to (q)uit, (c)ontinue or continue for (a)ll? "
            reply = input(p)
            if reply == "c" or reply == "q" or reply == "a":
                break
        return reply

