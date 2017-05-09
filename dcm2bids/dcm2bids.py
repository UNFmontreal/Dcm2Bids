# -*- coding: utf-8 -*-


import glob
import os
from .dcm2niix import Dcm2niix
from .sidecarparser import Sidecarparser
from .structure import Participant
from .utils import load_json, make_directory_tree, splitext_


class Dcm2bids(object):
    """
    """

    def __init__(self, dicom_dir, config, clobber, participant, session=None):
        self.dicomDir = dicom_dir
        self.config = load_json(config)
        self.clobber = clobber
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
            self._move(acq)

        return 0


    def _move(self, acquisition):
        targetDir = os.path.join(
                os.getcwd(), self.participant.directory, acquisition.dataType)
        filename = "{}_{}".format(self.participant.prefix, acquisition.suffix)
        targetBase = os.path.join(targetDir, filename)

        targetNiigz = targetBase + ".nii.gz"
        if not os.path.isfile(targetNiigz):
            make_directory_tree(targetDir)
            for f in glob.glob(acquisition.base + ".*"):
                _, ext = splitext_(f)
                os.rename(f, targetBase + ext)
        else:
            if self.clobber:
                print("'{}' overwrites".format(filename))
                for f in glob.glob(targetBase + ".*"):
                    os.remove(f)
                for f in glob.glob(acquisition.base + ".*"):
                    _, ext = splitext_(f)
                    os.rename(f, targetBase + ext)
            else:
                print("'{}' already exists".format(filename))

