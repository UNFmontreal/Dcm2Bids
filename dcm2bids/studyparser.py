# -*- coding: utf-8 -*-


from dicomparser import Dicomparser
import dcm2bids_utils as utils
import os


class TestRetestParser(Dicomparser):


    def __init__(self, dicomsDir):
        Dicomparser.__init__(self, dicomsDir)


    @property
    def excluded_dir_strings(self):
        return [
                '_ADC',
                '_COLFA',
                '_FA',
                '_TENSOR',
                '_TRACEW',
                ]


    def filter_acquisitions(self):
        for root, wrapper in self.get_wrappers(oneDcm=True):
            acquisition = {}
            self.wrapper = wrapper
            acquisition['directory'] = self.relpath(root)

            if self.is_in('FLAIR', 'SeriesDescription'):
                acquisition['data_type'] = 'anat'
                acquisition['suffix'] = 'FLAIR'

            elif self.is_in('T2', 'SeriesDescription'):
                acquisition['data_type'] = 'anat'
                acquisition['suffix'] = 'T2w'

            elif self.is_in('MPRAGE', 'SeriesDescription'):
                acquisition['data_type'] = 'anat'
                acquisition['suffix'] = 'T1w'

            elif self.is_in('DIFFUSION', 'ImageType'):
                if self.is_in('MOSAIC', 'ImageType'):
                    acquisition['data_type'] = 'dwi'
                    acquisition['suffix'] = 'dwi'
                else:
                    acquisition['data_type'] = 'fmap'
                    acquisition['suffix'] = 'epi'
                    if self.is_equal(1, 'CsaImage.PhaseEncodingDirectionPositive'):
                        acquisition['custom_labels'] = {'dir': 'ap'}
                    else:
                        acquisition['custom_labels'] = {'dir': 'pa'}

            else:
                acquisition['data_type'] = 'n/a'

            self.classifyDir(self.relpath(root), acquisition['data_type'])
            self._parameters.append(acquisition)


class ApneeMciParser(Dicomparser):


    def __init__(self, dicomsDir):
        Dicomparser.__init__(self, dicomsDir)
        self.echoTime = {
                1.64: '01',
                3.5: '02',
                5.36: '03',
                7.22: '04',
                }


    @property
    def excluded_dir_strings(self):
        return [
                '_FA',
                '_COLFA',
                '_ADC',
                '_TENSOR',
                '_TRACEW',
                'localizer',
                ]


    def filter_acquisitions(self):
        for root, wrapper in self.get_wrappers(oneDcm=True):
            acquisition = {}
            self.wrapper = wrapper
            acquisition['directory'] = self.relpath(root)

            if self.is_in('FLAIR', 'SeriesDescription'):
                acquisition['data_type'] = 'anat'
                acquisition['suffix'] = 'FLAIR'

            elif self.is_in('T2', 'SeriesDescription'):
                acquisition['data_type'] = 'anat'
                acquisition['suffix'] = 'T2w'

            elif self.is_in('MEMPRAGE', 'SeriesDescription'):
                acquisition['data_type'] = 'anat'
                acquisition['suffix'] = 'T1w'
                if self.is_equal(1, 'NumberOfAverages'):
                    num = self.echoTime[self.get_value('EchoTime')]
                    acquisition['custom_labels'] = {'acq': num}
                else:
                    acquisition['custom_labels'] = {'acq': 'RMS'}

            elif self.is_in('DIFFUSION', 'ImageType'):
                if self.is_in('MOSAIC', 'ImageType'):
                    acquisition['data_type'] = 'dwi'
                    acquisition['suffix'] = 'dwi'
                else:
                    acquisition['data_type'] = 'fmap'
                    acquisition['suffix'] = 'epi'
                    if self.is_equal(1, 'CsaImage.PhaseEncodingDirectionPositive'):
                        acquisition['custom_labels'] = {'dir': 'ap'}
                    else:
                        acquisition['custom_labels'] = {'dir': 'pa'}

            else:
                acquisition['data_type'] = 'n/a'

            self.classifyDir(self.relpath(root), acquisition['data_type'])
            self._parameters.append(acquisition)
