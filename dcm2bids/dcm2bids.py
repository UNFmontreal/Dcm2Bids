# -*- coding: utf-8 -*-


import glob
import logging
import os
from datetime import datetime
from .dcm2niix import Dcm2niix
from .sidecarparser import Sidecarparser
from .structure import Participant
from .utils import load_json, make_directory_tree, splitext_


class Dcm2bids(object):
    """
    """

    def __init__(
            self, dicom_dir, participant, config, output_dir=os.getcwd(),
            session=None, clobber=False, forceDcm2niix=False, log_level="INFO"):
        self.dicomDir = dicom_dir
        self.bidsDir = output_dir
        self.config = load_json(config)
        self.clobber = clobber
        self.forceDcm2niix = forceDcm2niix
        self.participant = Participant(participant, session)
        self._setLogger(log_level)
        self.logger.info("--- dcm2bids start ---")
        self.logger.info("participant: {}".format(participant))
        self.logger.info("session: {}".format(session))
        self.logger.info("config: {}".format(os.path.realpath(config)))
        self.logger.info(
                "BIDS directory: {}".format(os.path.realpath(output_dir)))
        self.logger.info("")


    @property
    def session(self):
        return self.participant.session

    @session.setter
    def session(self, value):
        self.participant.session = value


    def _setLogger(self, log_level):
        logDir = os.path.join(self.bidsDir, "log")
        logFile = "{0}_{1}.log".format(self.participant.prefix,
                datetime.now().strftime("%Y%m%dT%H%M%S"))
        make_directory_tree(logDir)
        logging.basicConfig(filename=os.path.join(logDir, logFile))
        self.logger = logging.getLogger("dcm2bids")
        self.logger.setLevel(log_level)


    def run(self):
        dcm2niix = Dcm2niix(self.dicomDir, self.bidsDir, self.participant)
        dcm2niix.run(self.forceDcm2niix)
        parser = Sidecarparser(dcm2niix.sidecars, self.config["descriptions"])

        self.logger.info("parsing sidecars")
        for acq in parser.acquisitions:
            self._move(acq)

        self.logger.info("--- dcm2bids finished without errors ---")
        return 0


    def _move(self, acquisition):
        targetDir = os.path.join(
                self.bidsDir, self.participant.directory, acquisition.dataType)
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
                print("Overwriting: {}".format(filename))
                for f in glob.glob(targetBase + ".*"):
                    os.remove(f)
                for f in glob.glob(acquisition.base + ".*"):
                    _, ext = splitext_(f)
                    os.rename(f, targetBase + ext)
            else:
                print("'{}' already exists, use --clobber to overwrite it".format(filename))

