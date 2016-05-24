# -*- coding: utf-8 -*-


import os


class Session(object):
    """
    """

    def __init__(self, json):
        self.__none = 'n/a'
        self.json = json
        self.name = self.__setName()
        self.sessionDir = ''


    def __setName(self):
        name = self.__none
        if self.json.has_key('session'):
            value = self.json['session']
            if value != self.__none:
                name = "ses-{}".format(value)
        return name


    def getName(self):
        return self.name


    def isSingle(self):
        return self.name == self.__none


    def setDir(self, bidsDir, participantName):
        path = os.path.join(bidsDir, participantName)
        if not self.isSingle():
            path = os.path.join(path, self.getName())
        self.sessionDir = path


    def getSessionDir(self):
        return self.sessionDir
