# -*- coding: utf-8 -*-

from batch import Batch
from session import Session
import os
import studyparser
import utils


class App(object):
    """
    """

    def __init__(self, args):
        self._bidsDir = args.bids_dir
        self._dicomDir = args.dicom_dir
        self._session = Session(args.session, args.participant, self._bidsDir)
        self._parser = getattr(studyparser, args.algorithm)(
                self._dicomDir, self._session)
        self._yes = args.yes
        self._codeDir = os.path.join(self._bidsDir, 'code')
        utils.make_directory_tree(self._codeDir)
        self._batch = Batch(self._codeDir, self._session)

    def run(self):
        utils.new_line()
        utils.info('Parse and group DICOM directory')
        self._parser.parse_acquisitions()

        utils.new_line()
        utils.info('Sort and set up acquisitions')
        self._parser.sort_acquisitions()

        #utils.new_line()
        #utils.ok('Acquisitions of interest:')
        #for _ in self._parser.caught: utils.info(_)

        utils.new_line()
        utils.warning('Acquisitions excluded:')
        for _ in self._parser._excluded:
            utils.info(_)

        utils.new_line()
        utils.info('Create YAML file for dcm2niibatch')
        for acq in self._parser.acquisitions:
            self._batch.add(acq)
        self._batch.write()

        utils.new_line()
        utils.ok('Batch file:')
        self._batch.show()

        if self._yes:
            launchBatch = True
        else:
            msg = "Do you want to launch dcm2niibatch ?"
            launchBatch = utils.query_yes_no(msg)

        if launchBatch:
            self._batch.launch()
            for acq in self._parser.acquisitions:
                acq.update_json()
        else:
            utils.new_line()
            utils.ok("To launch dcm2niibatch later:")
            utils.info("cd {}".format(self._codeDir))
            utils.info(self._batch.command)
        return 0
