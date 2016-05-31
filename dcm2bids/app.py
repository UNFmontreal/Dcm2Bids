# -*- coding: utf-8 -*-


from acquisition import Acquisition
from participant import Participant
import pprint
from session import Session
import studyparser
import dcm2bids_utils as utils


class App(object):
    """
    """


    def __init__(self, bidsDir, dicomsDir, description):
        self.bidsDir = bidsDir
        self.dicomsDir = dicomsDir
        self._description = description


    @property
    def participant(self):
        return Participant(self._description['participant'], self.bidsDir)


    @property
    def session(self):
        return Session(self._description['session'], self.participant)


    @property
    def acquisitions(self):
        for descriptionDict in self._description['acquisitions']:
            yield Acquisition(
                    descriptionDict, self.dicomsDir,
                    self.participant, self.session)


    def run(self):
        for acquisition in self.acquisitions:
            acquisition.convert()
            acquisition.writeJson()


    def searchAcqDesc(self, study):
        studyparserRef = {
                'apneemci': 'ApneeMciParser',
                'testretest': 'TestRetestParser',
                }
        parser = getattr(studyparser, studyparserRef[study])(self.dicomsDir)
        self._description['acquisitions'] = parser.filter_acquisitions()
        utils.info('Acquisitions description')
        pprint.pprint(self._description['acquisitions'])
