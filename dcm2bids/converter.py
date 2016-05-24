# -*- coding: utf-8 -*-


from subprocess import call

import utils


class Converter(object):
    """
    """

    def __init__(self):
        baseTpl = "mrconvert '{0}' {1}.nii.gz -force -quiet"
        dwiTpl = " -export_grad_mrtrix {1}.b -export_grad_fsl {1}.bvec {1}.bval"
        self.mrconvertTpl = {
                'anat': baseTpl,
                'dwi': baseTpl + dwiTpl,
                'fmap': baseTpl,
                'func': "", #TODO
                }


    def convert(self, acquisition, participantName):
        cmdTpl = self.mrconvertTpl[acquisition.getDataType()]
        dicomsDir = acquisition.getDicomsDir()
        outputDir = acquisition.getOutputDir()
        utils.makedirs(outputDir)
        outputWithoutExt = acquisition.getOutputWithoutExt()
        call(cmdTpl.format(dicomsDir, outputWithoutExt), shell=True)
