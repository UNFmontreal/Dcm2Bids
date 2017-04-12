# -*- coding: utf-8 -*-


import os
import json
from .batch import Batch
from .dcmparser import Dcmparser
from .structure import Acquisition, Participant


def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


class Dcm2bids(object):
    """
    """

    def __init__(self, bids_dir, dicom_dir, config, participant,
            session=None, dryrun=False):
        self.dicomDir = dicom_dir
        self.config = load_json(config)
        self.participant = Participant(participant, session)
        self.batch = Batch(
                self.config["batch_options"], bids_dir, self.participant)
        self.dryrun = dryrun


    @property
    def session(self):
        return self.participant.session

    @session.setter
    def session(self, value):
        self.participant.session = value


    def acquisitions(self):
        for root, dirs, files in os.walk(self.dicomDir):
            for f in sorted(files):
                if f.startswith('.') == True:
                    continue
                else:
                    dicomPath = os.path.join(root, f)
                    dcm = Dcmparser(dicomPath)
                    if dcm.isDicom():
                        yield dcm.search_from(self.config["descriptions"])
                        break
                    else:
                        continue


    def run(self):
        for acquisition in self.acquisitions():
            if acquisition is not None:
                self.batch.add(acquisition)
            else:
                pass
        self.batch.write()
        if self.dryrun:
            self.batch.show()
        else:
            self.batch.execute()
        return 0

