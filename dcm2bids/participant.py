# -*- coding: utf-8 -*-


import os


class Participant(object):
    """
    """

    def __init__(self, name, bidsDir):
        self._name = name
        self._bidsDir = bidsDir

    @property
    def name(self):
        return "sub-{}".format(self._name)

    @property
    def directory(self):
        return os.path.join(self._bidsDir, self.name)
