# -*- coding: utf-8 -*-


from future.utils import iteritems
import dicom
from dicom.errors import InvalidDicomError
from .structure import Acquisition


class Dcmparser(object):

    def __init__(self, dicomPath):
        self.ds = None
        self.dicomPath = dicomPath


    def isDicom(self):
        try:
            self.ds = dicom.read_file(self.dicomPath)
        except InvalidDicomError:
            self.ds = None
        return self.ds is not None


    def search_from(self, descriptions):
        for description in descriptions:
            if self._respect(description["criteria"]):
                acq = Acquisition(
                        self.dicomPath,
                        description["dataType"],
                        description["suffix"])
                if "customLabels" in description:
                    acq.customLabels = description["customLabels"]
                else:
                    acq.customLabels = None
                return acq
        #No criteria respecting the dicom informations
        return None


    def _respect(self, criteria):
        isEqual = "equal" in criteria
        isIn = "in" in criteria

        # Check if there is some criteria
        if not any([isEqual, isIn]):
            return False

        if isEqual:
            rsl_equal = self._isEqual(criteria["equal"])
        else:
            rsl_equal = True

        if isIn:
            rsl_in = self._isIn(criteria["in"])
        else:
            rsl_in = True

        return all([rsl_equal, rsl_in])


    def _isEqual(self, criteria):
        rsl = []
        for tag, query in iteritems(criteria):
            rsl.append(query == self.get_value(tag))
        return all(rsl)


    def _isIn(self, criteria):
        rsl = []
        for tag, query in iteritems(criteria):
            if isinstance(query, list):
                for q in query:
                    rsl.append(q in self.get_value(tag))
            else:
                rsl.append(query in self.get_value(tag))
        return all(rsl)


    def get_value(self, tag):
        if tag == "dicomPath":
            return self.dicomPath
        elif tag in self.ds:
            return self.ds.data_element(tag).value
        else:
            return None

