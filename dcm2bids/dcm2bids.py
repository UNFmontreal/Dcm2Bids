# -*- coding: utf-8 -*-


import logging
import os
import platform
import sys
from datetime import datetime
from glob import glob
from .dcm2niix import Dcm2niix
from .logger import setup_logging
from .sidecar import Sidecar, SidecarPairing
from .structure import Participant
from .utils import (
        DEFAULT,
        load_json,
        save_json,
        run_shell_command,
        splitext_,
        )
from .version import __version__, check_latest, dcm2niix_version


class Dcm2bids(object):
    """ Object to handle dcm2bids execution steps

    Args:
        dicom_dir (str or list): A list of folder with dicoms to convert
        participant (str): Label of your participant
        config (path): Path to a dcm2bids configuration file
        output_dir (path): Path to the BIDS base folder
        session (str): Optional label of a session
        clobber (boolean): Overwrite file if already in BIDS folder
        forceDcm2niix (boolean): Forces a cleaning of a previous execution of
                                 dcm2niix
        log_level (str): logging level
    """

    def __init__(
            self, dicom_dir, participant, config, output_dir=DEFAULT.outputDir,
            session=DEFAULT.session, clobber=DEFAULT.clobber,
            forceDcm2niix=DEFAULT.forceDcm2niix, log_level=DEFAULT.logLevel,
            **_):
        self._dicomDirs = []

        self.dicomDirs = dicom_dir
        self.bidsDir = output_dir
        self.config = load_json(config)
        self.participant = Participant(participant, session)
        self.clobber = clobber
        self.forceDcm2niix = forceDcm2niix
        self.logLevel = log_level

        #logging setup
        self.set_logger()

        self.logger.info("--- dcm2bids start ---")
        self.logger.info("OS:version: {}".format(platform.platform()))
        self.logger.info("python:version: {}".format(
            sys.version.replace("\n","")))
        self.logger.info("dcm2bids:version: {}".format(__version__))
        self.logger.info("dcm2niix:version: {}".format(dcm2niix_version()))
        self.logger.info("participant: {}".format(self.participant.name))
        self.logger.info("session: {}".format(self.participant.session))
        self.logger.info("config: {}".format(os.path.realpath(config)))
        self.logger.info(
                "BIDS directory: {}".format(os.path.realpath(output_dir)))


    @property
    def dicomDirs(self):
        return self._dicomDirs


    @dicomDirs.setter
    def dicomDirs(self, value):
        if isinstance(value, list):
            self._dicomDirs = value
        else:
            self._dicomDirs = [value,]


    def set_logger(self):
        """ Set a basic logger"""
        logDir = os.path.join(self.bidsDir, DEFAULT.tmpDirName, "log")
        logFile = os.path.join(logDir, "{}_{}.log".format(
                self.participant.prefix, datetime.now().isoformat()))

        #os.makedirs(logdir, exist_ok=True)
        #python2 compatibility
        if not os.path.exists(logDir):
            os.makedirs(logDir)

        setup_logging(self.logLevel, logFile)
        self.logger = logging.getLogger(__name__)


    def run(self):
        """
        """
        dcm2niix = Dcm2niix(self.dicomDirs, self.bidsDir, self.participant,
                self.config.get("dcm2niixOptions", DEFAULT.dcm2niixOptions))
        dcm2niix.run(self.forceDcm2niix)

        sidecars = []
        for filename in dcm2niix.sidecarFiles:
            sidecars.append(Sidecar(
                filename, self.config.get("compKeys", DEFAULT.compKeys)))
        sidecars = sorted(sidecars)

        parser = SidecarPairing(sidecars, self.config["descriptions"],
                self.config.get("searchMethod", DEFAULT.searchMethod))
        parser.build_graph()
        parser.build_acquisitions(self.participant)
        parser.find_runs()

        self.logger.info("moving acquisitions into BIDS folder")
        for acq in parser.acquisitions:
            self.move(acq)

        check_latest()
        check_latest("dcm2niix")

        return os.EX_OK


    def move(self, acquisition):
        """
        """
        for srcFile in glob(acquisition.srcRoot + ".*"):
            root, ext = splitext_(srcFile)
            dstFile = os.path.join(self.bidsDir, acquisition.dstRoot + ext)

            #os.makedirs(os.path.dirname(dstFile), exist_ok=True)
            #python2 compatibility
            if not os.path.exists(os.path.dirname(dstFile)):
                os.makedirs(os.path.dirname(dstFile))

            #checking if destination file exists
            if os.path.isfile(dstFile):
                self.logger.info("'{}' already exists".format(dstFile))

                if self.clobber:
                    self.logger.info("Overwriting because of 'clobber' option")

                else:
                    self.logger.info("Use clobber option to overwrite")
                    continue

            #it's an anat nifti file and the user using a deface script
            if (
                    self.config.get("defaceTpl")
                    and acquisition.dataType=="anat"
                    and ".nii" in ext):
                try:
                    os.remove(dstFile)
                except:
                    pass
                defaceTpl = self.config.get("defaceTpl")
                cmd = defaceTpl.format(srcFile=srcFile, dstFile=dstFile)
                run_shell_command(cmd)

            #use
            elif ext == ".json":
                data = acquisition.dstSidecarData(self.config["descriptions"])
                save_json(dstFile, data)
                os.remove(srcFile)

            #just move
            else:
                os.rename(srcFile, dstFile)

