# -*- coding: utf-8 -*-

from __future__ import print_function

from acquisition import Acquisition
from batch import Batch
from converter import Converter
from participant import Participant
from session import Session

import studyparser
import dcm2bids_utils as utils

import os
import pprint


class App(object):
    """
    """


    def __init__(self, bidsDir, dicomDir, description, algorithm):
        self._bidsDir = bidsDir
        self._dicomDir = dicomDir
        self._description = description
        #self._algorithm = algorithm
        self.parser = getattr(studyparser, algorithm)(self._dicomDir)


    @property
    def codeDir(self):
        codeDir = os.path.join(self._bidsDir, 'code')
        utils.make_directory_tree(codeDir)
        return codeDir


    @property
    def participant(self):
        return Participant(self._description['participant'], self._bidsDir)


    @property
    def session(self):
        return Session(self._description['session'], self.participant)


    @property
    def acquisitions(self):
        for descriptionDict in self._description['acquisitions']:
            yield Acquisition(
                    descriptionDict, self._dicomDir,
                    self.participant, self.session)


    @property
    def filename(self):
        filename = self.participant.name
        if not self.session.isSingle():
            filename += '_{}'.format(self.session.name)
        return filename


    def run(self):
        self.parseDicomDir()
        self.batch = Batch(self.codeDir, self.filename)
        for acquisition in self.acquisitions:
            self.batch.add_acquisition(acquisition)
        self.batch.show()
        self.batch.write()
        if utils.query_yes_no("Do you want to launch dcm2niibatch ?"):
            self.batch.convert()
        else:
            msg = "Launch dcm2niibatch form code directory:\n{}"
            utils.info(msg.format(self.batch.command))
            return 0
        return 0


    def parseDicomDir(self):
        utils.info('Parse and group DICOM directory')
        self.parser.parse_and_group()
        for key, group in self.parser.groups.iteritems():
            if self.isFromOneDirectory(group):
                pass
            else:
                self.info("Not in the same directory: {}".format(group))
        utils.info('Classifying')
        self._description['acquisitions'] = self.parser.classify()
        self.show_directories()
        #utils.info('Acquisitions description')
        #pprint.pprint(self._description['acquisitions'])


    def isFromOneDirectory(self, group):
        directory = set()
        for ds, meta, f in group:
            directory.add(os.path.dirname(f))
        return len(directory) == 1


    def show_directories(self):
        utils.ok('Series of interest:')
        print(*self.parser.caughtSeries, sep="\n")
        utils.fail('Series ignored:')
        print(*self.parser.ignoredSeries, sep="\n")
