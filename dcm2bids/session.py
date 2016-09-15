# -*- coding: utf-8 -*-


from participant import Participant
import os


class Session(object):
    """
    """

    def __init__(self, name, participant, bidsDir):
        self._name = name
        self._participant = Participant(participant, bidsDir)

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

    @property
    def prefix(self):
        prefix = self._participant.name
        if self.isSingle():
            return prefix
        else:
            return '{}_{}'.format(prefix, self.name)

    def isSingle(self):
        return self.name == None
