# -*- coding: utf-8 -*-


import os
from ..session import Session


class TestSession():

    def __init__(self):
        self.participantDir = os.path.join('bidsDir', 'participantName')
        self.sessionName = 'sessionName'
        self.sessionNA = Session(self.participantDir, None)
        self.session = Session(self.participantDir, self.sessionName)

    def test_attributes(self):
        assert self.sessionNA.name == None
        assert self.sessionNA.directory == self.participantDir
        print self.sessionNA.name, self.sessionNA.directory
        print self.session.name, self.session.directory
        assert self.session.name == 'ses-{}'.format(self.sessionName)
        assert self.session.directory == os.path.join(
                self.participantDir, 'ses-{}'.format(self.sessionName))
