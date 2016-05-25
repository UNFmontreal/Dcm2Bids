# -*- coding: utf-8 -*-


from subprocess import call
import dcm2bids_utils as utils


class Converter(object):
    """
    """

    def __init__(self):
        self.cmdTemplate = 'dcm2niix -o "{}" -f {} -z y "{}"'


    def convert(self, outputDir, filename, dicomsDir):
        utils.makedirs(outputDir)
        utils.info('Convert {}'.format(filename))
        cmd = self.cmdTemplate.format(outputDir, filename, dicomsDir)
        call(cmd, shell=True)
