# -*- coding: utf-8 -*-


import glob
import os
import datetime
import logging
from collections import OrderedDict
from .dcm2niix import Dcm2niix
from .sidecarparser import Sidecarparser
from .structure import Participant
from .utils import load_json, make_directory_tree, splitext_, save_json, write_txt, read_participants, write_participants
from subprocess import call


class Dcm2bids(object):
    """
    """

    def __init__(self, dicom_dir, config, clobber, participant, session=None,
                 selectseries=None, outputdir=os.getcwd(), loglevel="INFO", anonymizer=None):
        self.dicom_dir = dicom_dir
        self.config = load_json(config)
        self.clobber = clobber
        self.extension = '.nii.gz'
        self.participant = Participant(participant, session)
        self.selectseries = selectseries
        derivdir = os.path.join(outputdir, "derivatives")
        self.outputdir = os.path.join(outputdir,"sourcedata")
        self.dicomdir = os.path.join(outputdir,'tmp_dcm2bids')
        self.anonymizer = anonymizer
        if not os.path.exists(self.outputdir):
            os.makedirs(self.outputdir)
        if not os.path.exists(derivdir):
            os.makedirs(derivdir)
        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%Y/%m/%d %H:%M', filemode='a',
                            filename=os.path.join(
                                os.path.split(self.outputdir)[0],'dcm2bids.log'))
        self.logger = logging.getLogger("dcm2bids")
        self.logger.setLevel(loglevel.upper())
        self.logger.info("--- dcm2bids start ---")
        self.logger.info("participant: %s",participant)
        self.logger.info("session: %s",session)
        [self.logger.info("dicom_dir: %s",os.path.realpath(thisdir)) for thisdir in dicom_dir]
        self.logger.info("config: %s",os.path.realpath(config))
        self.logger.info("outputdir: %s",os.path.realpath(self.outputdir))

    @property
    def session(self):
        return self.participant.session

    @session.setter
    def session(self, value):
        self.participant.session = value


    def run(self):
        # convert dicoms to temporary dir

        self.logger.info("running dcm2niix DICOM to NIFTI conversion")
        dcm2niix = Dcm2niix(self.dicom_dir, self.participant, outputdir=self.dicomdir)
        dcm2niix.run()

        self.logger.info("parsing sidecars")
        parser = Sidecarparser(dcm2niix.sidecars,
                               self.config["descriptions"], self.selectseries)

        self.logger.info("moving acquisitions into BIDS output directory")
        for acq in parser.acquisitions:
            self._move(acq)

        self.logger.info("updating standard study files")
        if parser.acquisitions:
            self._updatestudyfiles()
        self.logger.info("--- dcm2bids finished without errors ---")
        return 0


    def _move(self, acquisition):
        targetDir = os.path.join(
                self.outputdir, self.participant.directory, acquisition.dataType)
        filename = "{}_{}".format(self.participant.prefix, acquisition.suffix)
        targetBase = os.path.join(targetDir, filename)

        # need to test for both because dcm2niix sometimes refuses to compress
        if os.path.isfile(targetBase + ".nii.gz") or os.path.isfile(targetBase + ".nii"):
            if self.clobber:
                print("'{}' overwrites".format(filename))
                for f in glob.glob(targetBase + ".*"):
                    os.remove(f)
                for f in glob.glob(acquisition.base + ".*"):
                    _, ext = splitext_(f)
                    os.rename(f, targetBase + ext)
            else:
                print("'{}' already exists".format(filename))
                return
        # if we make it this far, we can copy away
        make_directory_tree(targetDir)
        for f in glob.glob(acquisition.base + ".*"):
            _, ext = splitext_(f)
            if self.anonymizer and acquisition.dataType=='anat' and ".nii" in ext:
                # it's an anat scan - try the anonymizer
                command = " ".join([self.anonymizer,f,targetBase + ext])
                self.logger.info("anonymizing anatomical with %s: %s",
                                 self.anonymizer,targetBase + ext)
                call(command, shell=True)
            else:
                # just move
                os.rename(f, targetBase + ext)


    def _updatestudyfiles(self):
        # participant table
        partfile = os.path.join(self.outputdir,"participants.tsv")
        participants = read_participants(partfile)
        if not participants or not any([part["participant_id"]==self.participant.name
                                        for part in participants]):
            participants.append(
                OrderedDict(zip(("participant_id","age","sex","group"),
                                (self.participant.name,"n/a","n/a","n/a"))))
            write_participants(partfile, participants)

        # dataset description
        descfile = os.path.join(self.outputdir,'dataset_description.json')
        if not os.path.exists(descfile):
            save_json({"Name": "", "BIDSVersion": "1.0.1",
                        "License": "", "Authors": [""],
                        "Acknowledgments": "",
                        "HowToAcknowledge": "",
                        "Funding": "",
                        "ReferencesAndLinks": [""],
                        "DatasetDOI": ""}, descfile)

        # readme/change files
        readmefile = os.path.join(self.outputdir,'README')
        if not os.path.exists(readmefile):
            write_txt(readmefile)
        changefile = os.path.join(self.outputdir,'CHANGES')
        if not os.path.exists(changefile):
            write_txt(changefile,
                      ["Revision history for BIDS dataset.",
                       "",
                       "0.01 " + datetime.date.today().strftime("%Y-%m-%d"),
                       "",
                       " - Initialised study directory"])
