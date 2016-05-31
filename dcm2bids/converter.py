# -*- coding: utf-8 -*-


from subprocess import call
import dcm2bids_utils as utils
import os


class Converter(object):
    """
    """


    def __init__(self):
        self.cmdTemplate = 'dcm2niix -o "{}" -f {} -z y "{}"'


    def convert(self, outputDir, filename, dicomsDir):
        self.make_directory_tree(outputDir)
        utils.info('Convert {}'.format(filename))
        cmd = self.cmdTemplate.format(outputDir, filename, dicomsDir)
        call(cmd, shell=True)


    @staticmethod
    def make_directory_tree(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
