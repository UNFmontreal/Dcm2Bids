# -*- coding: utf-8 -*-


from dicomparser import Dicomparser
import dcm2bids_utils as utils
import os


class DefaultParser(Dicomparser):


    def __init__(self, dicomsDir):
        Dicomparser.__init__(self, dicomsDir)
        self.excludedSeries = [
                'PD',
                '_ADC',
                '_COLFA',
                '_ColFA',
                '_FA',
                '_TENSOR',
                '_TRACEW',
                ]


    def filter_acquisitions(self, root, wrapper):
        parameter = {}
        self.wrapper = wrapper
        parameter['directory'] = root

        if self.is_in('FLAIR', 'SeriesDescription'):
            parameter['data_type'] = 'anat'
            parameter['suffix'] = 'FLAIR'

        elif self.is_in('T2', 'SeriesDescription'):
            parameter['data_type'] = 'anat'
            parameter['suffix'] = 'T2w'

        elif self.is_in('MPRAGE', 'SeriesDescription'):
            parameter['data_type'] = 'anat'
            parameter['suffix'] = 'T1w'

        elif self.is_in('DIFFUSION', 'ImageType'):
            if self.is_in('MOSAIC', 'ImageType'):
                parameter['data_type'] = 'dwi'
                parameter['suffix'] = 'dwi'
            else:
                #self.log_metadata(self.wrapper, root)
                parameter['data_type'] = 'fmap'
                parameter['suffix'] = 'epi'
                #print self.get_value('CsaImage.PhaseEncodingDirectionPositive')
                if self.is_equal(1, 'CsaImage.PhaseEncodingDirectionPositive'):
                    parameter['custom_labels'] = {'dir': 'ap'}
                elif self.is_equal(0, 'CsaImage.PhaseEncodingDirectionPositive'):
                    parameter['custom_labels'] = {'dir': 'pa'}
                elif self.is_in('AP', 'SeriesDescription'):
                    parameter['custom_labels'] = {'dir': 'ap'}
                elif self.is_in('PA', 'SeriesDescription'):
                    parameter['custom_labels'] = {'dir': 'pa'}
                else:
                    parameter['data_type'] = 'n/a'

        else:
            parameter['data_type'] = 'n/a'

        return parameter


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


    def filter_parameters(self):
        for root, wrapper in self.get_wrappers(oneDcm=True):
            parameter = {}
            self.wrapper = wrapper
            parameter['directory'] = self.relpath(root)

            if self.is_in('FLAIR', 'SeriesDescription'):
                parameter['data_type'] = 'anat'
                parameter['suffix'] = 'FLAIR'

            elif self.is_in('T2', 'SeriesDescription'):
                parameter['data_type'] = 'anat'
                parameter['suffix'] = 'T2w'

            elif self.is_in('MEMPRAGE', 'SeriesDescription'):
                parameter['data_type'] = 'anat'
                parameter['suffix'] = 'T1w'
                if self.is_equal(1, 'NumberOfAverages'):
                    num = self.echoTime[self.get_value('EchoTime')]
                    parameter['custom_labels'] = {'acq': num}
                else:
                    parameter['custom_labels'] = {'acq': 'RMS'}

            elif self.is_in('DIFFUSION', 'ImageType'):
                if self.is_in('MOSAIC', 'ImageType'):
                    parameter['data_type'] = 'dwi'
                    parameter['suffix'] = 'dwi'
                else:
                    parameter['data_type'] = 'fmap'
                    parameter['suffix'] = 'epi'
                    if self.is_equal(1, 'CsaImage.PhaseEncodingDirectionPositive'):
                        parameter['custom_labels'] = {'dir': 'ap'}
                    else:
                        parameter['custom_labels'] = {'dir': 'pa'}

            else:
                parameter['data_type'] = 'n/a'

            self.classifyDir(self.relpath(root), parameter['data_type'])
            self._parameters.append(parameter)
