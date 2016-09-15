# -*- coding: utf-8 -*-


from acquisition import Acquisition
import dcmstack
import dicom
from dicom.errors import InvalidDicomError
import os
import utils


class Dicomparser(object):
    """
    """

    def __init__(self, dicomDir, session):
        self._dicomDir = dicomDir
        self._session = session
        self._caught = set()
        self._excluded = set()
        self._acquisitions = []

    @property
    def caught(self):
        return self._caught

    @property
    def excluded(self):
        return self._excluded

    @property
    def acquisitions(self):
        return self._acquisitions


    def parse_acquisitions(self):
        src_paths = []
        for f in self._files:
            # Check if it is a DICOM
            try:
                ds = dicom.read_file(f)
            except InvalidDicomError:
                utils.warning('Not a DICOM file: {}'.format(f))
                continue
            # Filter by serie description
            dsDesc = ds.SeriesDescription
            if any(_ in dsDesc for _ in self.exclusionCriteria):
                self._excluded.add(dsDesc)
            else:
                src_paths.append(f)
        groups = dcmstack.parse_and_group(src_paths)

        for key, group in groups.iteritems():
            if self._isFromOneDirectory(group):
                #utils.ok("Same directory: {}".format(key[2]))
                stack = dcmstack.stack_group(group)
                inDir = os.path.dirname(group[0][2])
                self._acquisitions.append(
                        Acquisition(inDir, stack, self._session))
            else:
                #TODO: regroup dicoms in a tmp directory
                utils.new_line()
                utils.fail("DICOM of '{}' are not in the same directory.\nThis structure won't be compatible with dcm2niibatch".format(key[2]))

    @property
    def _files(self):
        for root, dirs, files in os.walk(self._dicomDir):
            for f in files:
                if f.startswith('.') == True:
                    pass
                else:
                    yield os.path.join(root, f)

    def _isFromOneDirectory(self, group):
        directory = set()
        for ds, meta, f in group:
            directory.add(os.path.dirname(f))
        return len(directory) == 1


    def sort_acquisitions(self):
        sortedAcquisitions = []
        for acq in self._acquisitions:
            self._wrapper = acq.wrapper
            acq.description = self.get_value('SeriesDescription')
            self.setup_criteria(acq)
            if acq.dataType == 'n/a':
                self._excluded.add(acq.description)
            else:
                self._caught.add(acq.description)
                sortedAcquisitions.append(acq)
        self._acquisitions = sortedAcquisitions

    #~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # Utils for setup_criteria #
    #~~~~~~~~~~~~~~~~~~~~~~~~~~#
    exclusionCriteria = []

    def get_value(self, key):
        return self._wrapper.meta_ext.get_values(key)

    def setup_criteria(self):
        """ Set by studyparser
        """
        pass

