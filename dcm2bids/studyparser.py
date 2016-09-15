# -*- coding: utf-8 -*-


from dicomparser import Dicomparser
import utils
import os


class DefaultParser(Dicomparser):


    def __init__(self, dicomsDir, session):
        Dicomparser.__init__(self, dicomsDir, session)
        self.exclusionCriteria = [
                'PD',
                '_ADC',
                '_COLFA',
                '_ColFA',
                '_FA',
                '_TENSOR',
                '_TRACEW',
                ]


    def setup_criteria(self, acq):

        imageType = self.get_value('ImageType')
        phaseEncoding = self.get_value(
                'CsaImage.PhaseEncodingDirectionPositive')

        if 'FLAIR' in acq.description:
            acq.dataType = 'anat'
            acq.suffix = 'FLAIR'

        elif 'T2' in acq.description:
            acq.dataType = 'anat'
            acq.suffix = 'T2w'

        elif 'MPRAGE' in acq.description:
            acq.dataType = 'anat'
            acq.suffix = 'T1w'

        elif 'DIFFUSION' in imageType:
            if 'MOSAIC' in imageType:
                acq.dataType = 'dwi'
                acq.suffix = 'dwi'
            else:
                acq.dataType = 'fmap'
                acq.suffix = 'epi'
                if 1 == phaseEncoding:
                    acq.customLabels = {'dir': 'ap'}
                elif 0 == phaseEncoding:
                    acq.customLabels = {'dir': 'pa'}
                elif 'AP' in acq.description:
                    acq.customLabels = {'dir': 'ap'}
                elif 'PA' in acq.description:
                    acq.customLabels = {'dir': 'pa'}
                else:
                    acq.dataType = 'n/a'

        else:
            acq.dataType = 'n/a'


class ApneeMciParser(Dicomparser):


    def __init__(self, dicomsDir, session):
        Dicomparser.__init__(self, dicomsDir, session)
        self.exclusionCriteria = [
                '_FA',
                '_COLFA',
                '_ADC',
                '_TENSOR',
                '_TRACEW',
                'localizer',
                ]
        self.echoTime = {
                1.64: '01',
                3.5: '02',
                5.36: '03',
                7.22: '04',
                }


    def setup_criteria(self, acq):

        imageType = self.get_value('ImageType')
        phaseEncoding = self.get_value(
                'CsaImage.PhaseEncodingDirectionPositive')

        if 'FLAIR' in acq.description:
            acq.dataType = 'anat'
            acq.suffix = 'FLAIR'

        elif 'T2' in acq.description:
            acq.dataType = 'anat'
            acq.suffix = 'T2w'

        elif 'MPRAGE' in acq.description:
            acq.dataType = 'anat'
            acq.suffix = 'T1w'
            if 1 == self.get_value('NumberOfAverages'):
                num = self.echoTime[self.get_value('EchoTime')]
                acq.customLabels = {'acq': num}
            else:
                acq.customLabels = {'acq': 'RMS'}

        elif 'DIFFUSION' in imageType:
            if 'MOSAIC' in imageType:
                acq.dataType = 'dwi'
                acq.suffix = 'dwi'
            else:
                acq.dataType = 'fmap'
                acq.suffix = 'epi'
                if 1 == phaseEncoding:
                    acq.customLabels = {'dir': 'ap'}
                elif 0 == phaseEncoding:
                    acq.customLabels = {'dir': 'pa'}
                elif 'AP' in acq.description:
                    acq.customLabels = {'dir': 'ap'}
                elif 'PA' in acq.description:
                    acq.customLabels = {'dir': 'pa'}
                else:
                    acq.dataType = 'n/a'

        else:
            acq.dataType = 'n/a'
