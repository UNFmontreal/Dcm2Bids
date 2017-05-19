# -*- coding: utf-8 -*-


import glob
import os
from subprocess import call
from collections import OrderedDict
import re
from .utils import clean


def sidecar2meta(carfile):
    """extract series number and potential
    suffixes (reflecting e.g. separate images for each echo) from the dcm2niix
    sidecar file name"""
    hits = re.search("_series(?P<series>\d{3})(?P<suffix>\w*).json",
                     os.path.split(carfile)[1])
    return {"seriesnum": int(hits.group("series")), "suffix": hits.group("suffix")}


class Dcm2niix(object):
    """
    """

    def __init__(self, dicom_dir, participant=None, output="dcm2niix-example",
                 outputdir=os.path.join(os.getcwd(), 'tmp_dcm2bids')):
        self.dicomDir = dicom_dir
        self.participant = participant
        self.output = output
        self.outputdir = outputdir
        if not os.path.exists(self.outputdir):
            os.makedirs(self.outputdir)
        self.options = "-b y -ba y -z y -f '%f_%p_%t_series%3s'"
        self.sidecars = []

    @property
    def outputDir(self):
        if self.participant is None:
            return os.path.join(self.outputdir, self.output)
        else:
            return os.path.join(self.outputdir, self.participant.prefix)


    def run(self):
        clean(self.outputDir)
        self.execute()
        carfiles = glob.glob(os.path.join(self.outputDir, "*.json"))
        carfiles.sort()
        self.sidecars = OrderedDict((thiscar,sidecar2meta(thiscar))
                                    for thiscar in carfiles)
        return 0


    def execute(self):
        for directory in self.dicomDir:
            commandStr = "dcm2niix {} -o {} {}"
            command = commandStr.format(self.options, self.outputDir, directory)
            call(command, shell=True)
