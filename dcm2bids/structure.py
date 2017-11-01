# -*- coding: utf-8 -*-


import os


class Participant(object):
    """
    """

    def __init__(self, name, session=None):
        self._name = name
        self._session = session


    @property
    def name(self):
        return "sub-{}".format(self._name)


    @property
    def session(self):
        if self._session is None:
            return None
        else:
            return 'ses-{}'.format(self._session)

    @session.setter
    def session(self, session):
        self._session = session


    @property
    def directory(self):
        if self.hasSession():
            return os.path.join(self.name, self.session)
        else:
            return self.name


    @property
    def prefix(self):
        if self.hasSession():
            return '{}_{}'.format(self.name, self.session)
        else:
            return self.name


    def hasSession(self):
        return self.session is not None



class Acquisition(object):
    """
    """

    def __init__(self, base, dataType, modalityLabel, customLabels=None):
        self.base = base
        self.dataType = dataType
        self._suffix = modalityLabel
        self.customLabels = customLabels


    @property
    def suffix(self):
        suffix = ''
        if self.customLabels:
            suffix += '{}_'.format(self.customLabels)
        suffix += self._suffix
        return suffix

