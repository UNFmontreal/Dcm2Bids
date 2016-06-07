# -*- coding: utf-8 -*-


from acquisition import Acquisition
from batch import Batch
from converter import Converter
from participant import Participant
from session import Session

import studyparser
import dcm2bids_utils as utils

import os
import pprint


class App(object):
    """
    """


    def __init__(self, bidsDir, dicomDir, description, algorithm):
        self._bidsDir = bidsDir
        self._dicomDir = dicomDir
        self._description = description
        self._algorithm = algorithm


    @property
    def codeDir(self):
        codeDir = os.path.join(self._bidsDir, 'code')
        utils.make_directory_tree(codeDir)
        return codeDir


    @property
    def participant(self):
        return Participant(self._description['participant'], self._bidsDir)


    @property
    def session(self):
        return Session(self._description['session'], self.participant)


    @property
    def acquisitions(self):
        for descriptionDict in self._description['acquisitions']:
            yield Acquisition(
                    descriptionDict, self._dicomDir,
                    self.participant, self.session)


    @property
    def filename(self):
        filename = self.participant.name
        if not self.session.isSingle():
            filename += '_{}'.format(self.session.name)
        return filename


    def run(self):
        self.parseDicomDir()
        self.batch = Batch()
        for acquisition in self.acquisitions:
            self.batch.add_acquisition(acquisition)
            #acquisition.writeJson()
        self.batch.show()
        filenamePath = os.path.join(self.codeDir, self.filename)
        self.batch.write(filenamePath)
        converter = Converter(filenamePath)
        if utils.query_yes_no("Do you want to launch dcm2niibatch ?"):
            converter.convert()
        else:
            utils.info("dcm2niibatch command line:\n{}".format(converter.command))
            return 0
        return 0


    def parseDicomDir(self):
        parser = getattr(studyparser, self._algorithm)(self._dicomDir)
        parser.filter_acquisitions()
        self._description['acquisitions'] = parser.parameters
        parser.show_directories()
        #utils.info('Acquisitions description')
        #pprint.pprint(self._description['acquisitions'])
