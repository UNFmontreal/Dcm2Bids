# -*- coding: utf-8 -*-


from subprocess import call
import dcm2bids_utils as utils


class Converter(object):
    """
    """


    def __init__(self, filename):
        #self.cmdTemplate = 'dcm2niix -o "{}" -f {} -z y "{}"'
        self._cmdTemplate = 'dcm2niibatch {}'
        self._filename = "{}.yaml".format(filename)


    @property
    def command(self):
        return self._cmdTemplate.format(self._filename)


    #def convert(self, outputDir, filename, dicomsDir):
    def convert(self):
        utils.info("running: {}".format(self.command))
        call(self.command, shell=True)
