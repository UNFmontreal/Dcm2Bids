# -*- coding: utf-8 -*-


from subprocess import call
import dcm2bids_utils as utils
import os
import pprint


class Batch(object):
    """
    """


    def __init__(self, codeDir, filename):
        self._codeDir = codeDir
        self._filename = "{}.yaml".format(filename)
        self._options = {
                "isGz": True,
                "isFlipY": False,
                "isVerbose": False,
                "isCreateBIDS": True,
                "isOnlySingleFile": False,
                }
        self._cmdTemplate = 'dcm2niibatch {}'
        self._files = []


    @property
    def data(self):
        return {"Options": self._options, "Files": self._files}


    @property
    def command(self):
        return self._cmdTemplate.format(self._filename)


    def add_acquisition(self, acquisition):
        self._files.append({
                "in_dir": os.path.relpath(acquisition.in_dir, self._codeDir),
                "out_dir": os.path.relpath(acquisition.out_dir, self._codeDir),
                "filename": acquisition.filename,
                })


    def show(self):
        utils.ok('Batch file:')
        pprint.pprint(self.data)


    def write(self):
        utils.write_yaml(self.data, os.path.join(self._codeDir, self._filename))


    def convert(self):
        os.chdir(self._codeDir)
        call(self.command, shell=True)
