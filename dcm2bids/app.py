# -*- coding: utf-8 -*-


import os

import utils
import converter
import session
import participant
import acquisition
import metainfo


class App(object):
    """
    """

    def __init__(self, output, jsonFile):
        self.bidsDir = os.path.abspath(output)
        self.masterDicomsDir = os.path.dirname(os.path.abspath(jsonFile))
        self.json = utils.loadJsonFile(jsonFile)
        self.participant = participant.Participant(self.json["participant"])
        self.session = session.Session(self.json)
        self.session.setDir(self.bidsDir, self.participant.getName())
        self.acquisitions = self.__setAcquisitions()
        self.converter = converter.Converter()


    def __setAcquisitions(self):
        acquisitions = []
        for description in self.json['acquisitions']:
            acq = acquisition.Acquisition(description, self.session)
            acq.setDicomsDir(self.masterDicomsDir)
            acq.setOutputWithoutExt(self.participant.getName())
            acquisitions.append(acq)
        return acquisitions


    def run(self):
        for acquisition in self.acquisitions:
            #self.converter.convert(acquisition, self.participant.getName())
            ds = utils.getDicomFromDir(acquisition.getDicomsDir())
            meta = metainfo.Metainfo(ds)
            meta.writeJsons(acquisition.getOutputWithouExt())
