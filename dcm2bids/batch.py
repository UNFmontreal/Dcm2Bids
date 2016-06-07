# -*- coding: utf-8 -*-


import dcm2bids_utils as utils
import os
import pprint


class Batch(object):
    """
    """


    def __init__(self):
        self._options = {
                "isGz": True,
                "isFlipY": False,
                "isVerbose": False,
                "isCreateBIDS": True,
                "isOnlySingleFile": False,
                }
        self._files = []


    @property
    def data(self):
        return {"Options": self._options, "Files": self._files}


    def add_acquisition(self, acquisition):
        self._files.append({
                "in_dir": acquisition.in_dir,
                "out_dir": acquisition.out_dir,
                "filename": acquisition.filename,
                })


    def show(self):
        utils.ok('Batch file:')
        pprint.pprint(self.data)


    def write(self, filename):
        utils.write_yaml(self.data, "{}.yaml".format(filename))
