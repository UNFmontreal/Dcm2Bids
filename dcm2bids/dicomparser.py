# -*- coding: utf-8 -*-


import dcmstack
import dcm2bids_utils as utils
import dicom
from dicom.errors import InvalidDicomError
import os


class Dicomparser(object):
    """
    """


    def __init__(self, dicomsDir):
        self._dicomsDir = dicomsDir
        self._caughtSeries = set()
        self._ignoredSeries = set()
        self._log = 0
        self.excludedSeries = []


    @property
    def caughtSeries(self):
        return self._caughtSeries


    @property
    def ignoredSeries(self):
        return self._ignoredSeries


    @property
    def groups(self):
        return self._groups


    @property
    def _wrappers(self):
        for key, group in self._groups.iteritems():
            stack = dcmstack.stack_group(group)
            root = os.path.dirname(group[0][2])
            yield (root, stack.to_nifti_wrapper())


    def filter_acquisitions(self):
        pass


    def classifySeries(self, description, dataType):
        if dataType == 'n/a':
            self._ignoredSeries.add(description)
        else:
            self._caughtSeries.add(description)


    @property
    def _files(self):
        for root, dirs, files in os.walk(self._dicomsDir):
            for f in files:
                if f.startswith('.') == True:
                    pass
                else:
                    yield os.path.join(root, f)


    def parse_and_group(self):
        src_paths = []
        for f in self._files:
            # Check if it is a DICOM
            try:
                ds = dicom.read_file(f)
            except InvalidDicomError:
                utils.fail('Not a DICOM: {}'.format(f))
                continue
            #
            dsDesc = ds.SeriesDescription
            if any(_ in dsDesc for _ in self.excludedSeries):
                self._ignoredSeries.add(dsDesc)
            else:
                src_paths.append(f)
        self._groups = dcmstack.parse_and_group(src_paths)


    def classify(self):
        parameters = []
        for root, wrapper in self._wrappers:
            parameter = self.filter_acquisitions(root, wrapper)
            description = self.get_value('SeriesDescription')
            dataType = parameter['data_type']
            self.classifySeries(description, dataType)
            if dataType != 'n/a':
                parameters.append(parameter)
        return parameters


    def get_value(self, key):
        return self.wrapper.meta_ext.get_values(key)


    def is_equal(self, value, key):
        return value == self.get_value(key)


    def is_in(self, value, key):
        return value in self.get_value(key)


    def log_metadata(self, wrapper, root):
        data  = wrapper.meta_ext._content
        data["aroot"] = root
        utils.write_json(data, "log{}.json".format(self._log))
        self._log += 1
