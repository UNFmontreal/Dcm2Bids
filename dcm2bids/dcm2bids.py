# -*- coding: utf-8 -*-


import glob
import logging
import os
from datetime import datetime
from .dcm2niix import Dcm2niix
from .sidecarparser import Sidecarparser
from .structure import Participant
from .utils import load_json, make_directory_tree, run_shell_command, splitext_
from subprocess import call


class Dcm2bids(object):
    """
    """

    def __init__(
            self, dicom_dir, participant, config, output_dir=os.getcwd(),
            session=None, clobber=False, forceDcm2niix=False, anonymizer=None,
            log_level="INFO"):
        self.dicomDirs = dicom_dir
        self.bidsDir = output_dir
        self.config = load_json(config)
        self.clobber = clobber
        self.forceDcm2niix = forceDcm2niix
        self.participant = Participant(participant, session)
        self.anonymizer = anonymizer
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
        logging.basicConfig()

        logDir = os.path.join(self.bidsDir, "log")
        logFile = "{0}_{1}.log".format(self.participant.prefix,
                datetime.now().strftime("%Y%m%dT%H%M%S"))
        make_directory_tree(logDir)

        #file handler
        handler = logging.FileHandler(os.path.join(logDir, logFile))

        #logger
        self.logger = logging.getLogger("dcm2bids")
        self.logger.setLevel(log_level)
        self.logger.addHandler(handler)


    def run(self):
        dcm2niix = Dcm2niix(self.dicomDirs, self.bidsDir, self.participant)
        dcm2niix.run(self.forceDcm2niix)
        parser = Sidecarparser(dcm2niix.sidecars, self.config["descriptions"])

        self.logger.info("moving acquisitions into BIDS output directory")
        for acq in parser.acquisitions:
            self._move(acq)

        #self.logger.info("updating standard study files")
        #if parser.acquisitions:
            #self._updatestudyfiles()

        return 0


    def _move(self, acquisition):
        def _anonOrRename():
            for f in glob.glob(acquisition.base + ".*"):
                _, ext = splitext_(f)
                if (self.anonymizer
                        and acquisition.dataType=='anat'
                        and ".nii" in ext):
                    # it's an anat scan - try the anonymizer
                    self.logger.info("")
                    cmd = "{0} {1} {2}".format(
                            self.anonymizer, f, targetBase+ext)
                    run_shell_command(cmd)
                else:
                    # just move
                    os.rename(f, targetBase+ext)

        targetDir = os.path.join(
                self.bidsDir, self.participant.directory, acquisition.dataType)
        filename = "{}_{}".format(self.participant.prefix, acquisition.suffix)
        targetBase = os.path.join(targetDir, filename)

        #need to test for both because dcm2niix sometimes refuses to compress
        targetExists = (os.path.isfile(targetBase + ".nii.gz")
                or os.path.isfile(targetBase + ".nii"))

        if targetExists:

            if self.clobber:
                self.logger.info("overwriting: {}".format(filename))
                for f in glob.glob(targetBase + ".*"):
                    os.remove(f)
                _anonOrRename()

            else:
                self.logger.info("'{}' already exists, use --clobber to overwrite it".format(filename))

        else:
            make_directory_tree(targetDir)
            _anonOrRename()
