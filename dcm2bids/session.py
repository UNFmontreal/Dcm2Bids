# -*- coding: utf-8 -*-


import os


class Session(object):
    """
    """

    def __init__(self, name, participant):
        self._name = name
        self._participant = participant


    @property
    def name(self):
        if self._name == 'n/a':
            return None
        else:
            return 'ses-{}'.format(self._name)


    @property
    def directory(self):
        path = self._participant.directory
        if self.isSingle():
            return path
        else:
            return os.path.join(path, self.name)


    def isSingle(self):
        return self.name == None
