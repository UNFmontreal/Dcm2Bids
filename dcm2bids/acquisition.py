# -*- coding: utf-8 -*-


import os


class Acquisition(object):
    """
    """

    def __init__(self, description, session):
        self.description = description
        self.session = session
        self.dataType = description["data_type"]
        self.suffix = self.__setSuffix()
        self.dicomsDir = ''
        self.outputWithoutExt = ''


    def __setSuffix(self):
        suffix = ""
        if not self.session.isSingle():
            suffix += "{}_".format(self.session.getName())
        if self.description.has_key("custom_labels"):
            for key, value in self.description["custom_labels"].iteritems():
                suffix += "{}-{}_".format(key, value)
        suffix += self.description["suffix"]
        return suffix


    def setDicomsDir(self, masterDicomsDir):
        self.dicomsDir = os.path.join(
                masterDicomsDir, self.description["directory"])


    def getDicomsDir(self):
        return self.dicomsDir


    def getDataType(self):
        return self.dataType


    def getOutputDir(self):
        return os.path.join(self.session.getSessionDir(), self.dataType)


    def setOutputWithoutExt(self, participantName):
        outputDir = self.getOutputDir()
        base = "{}_{}".format(participantName, self.suffix)
        self.outputWithoutExt = os.path.join(outputDir, base)


    def getOutputWithoutExt(self):
        return self.outputWithoutExt
