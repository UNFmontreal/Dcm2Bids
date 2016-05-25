# -*- coding: utf-8 -*-


from acquisition import Acquisition
from converter import Converter
from participant import Participant
from session import Session
import dcm2bids_utils as utils
#import metainfo


class App(object):
    """
    """

    def __init__(self, bidsDir, dicomsDir, description):
        self.bidsDir = bidsDir
        self.dicomsDir = dicomsDir
        self._description = description
        self._converter = Converter()


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
            self._convert(acquisition)
            #ds = utils.getDicomFromDir(acquisition.getDicomsDir())
            #meta = metainfo.Metainfo(ds)
            #meta.writeJsons(acquisition.getOutputWithouExt())


    def _convert(self, acquisition):
        outputDir = acquisition.outputDir
        filename = acquisition.filename
        dicomsDir = acquisition.dicomsDir
        self._converter.convert(outputDir, filename, dicomsDir)
