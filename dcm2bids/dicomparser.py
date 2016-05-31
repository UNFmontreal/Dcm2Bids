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


    def relpath(self, root):
        return os.path.relpath(root, self._dicomsDir)


    def get_wrappers(self, oneDcm):
        for root, files in self._child_directories(self._dicomsDir):
            if any(_ in root for _ in self.excluded_dir_strings):
                utils.fail('Excluded: {}'.format(self.relpath(root)))
                continue
            else:
                yield (root, self.get_wrapper(root, files, oneDcm))


    @staticmethod
    def _child_directories(directory):
        for root, dirs, files in os.walk(directory):
            if not dirs:
                yield (root, files)


    @staticmethod
    def get_wrapper(root, files, oneDcm):
        stack = dcmstack.DicomStack()
        for f in files:
            if f.startswith('.') == True:
                pass
            else:
                abspath = os.path.join(root, f)
                try:
                    src_dcm = dicom.read_file(abspath)
                    stack.add_dcm(src_dcm)
                    if oneDcm:
                        break
                    else:
                        continue
                except InvalidDicomError:
                    utils.fail('Is not a DICOM: {}'.format(abspath))
                    continue
        return stack.to_nifti_wrapper()


    def get_value(self, key):
        return self.wrapper.meta_ext.get_values(key)


    def is_equal(self, value, key):
        return value == self.get_value(key)


    def is_in(self, value, key):
        return value in self.get_value(key)


    def write(self, root, filename):
        files = os.listdir(root)
        wrapper = self.get_wrapper(root, files, False)
        utils.write_json(wrapper.meta_ext._content, filename)
