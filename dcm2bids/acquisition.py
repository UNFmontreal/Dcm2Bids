# -*- coding: utf-8 -*-


import os
import utils


class Acquisition(object):
    """
    """

    def __init__(self, inDir, stack, session=None):
        self._inDir = inDir
        self._stack = stack
        self._session = session
        self._dataType = None
        self._suffix = None
        self._customLabels = None
        self._description = None


    @property
    def filename(self):
        return "{}_{}".format(self._session.prefix, self.postfix)

    @property
    def inDir(self):
        return self._inDir

    @property
    def outDir(self):
        return os.path.join(self._session.directory, self.dataType)


    @property
    def wrapper(self):
        return self._stack.to_nifti_wrapper()


    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session= value


    @property
    def dataType(self):
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        self._dataType = value


    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        self._suffix = value


    @property
    def customLabels(self):
        return self._customLabels

    @customLabels.setter
    def customLabels(self, value):
        self._customLabels = value


    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value


    @property
    def postfix(self):
        postfix = ''
        if self.customLabels != None:
            for key, value in self.customLabels.iteritems():
                postfix += '{}-{}_'.format(key, value)
        postfix += self.suffix
        return postfix

    def update_json(self):
        jsonFile = os.path.join(self.out_dir, "{}.json".format(self.filename))
        data = utils.load_json(jsonFile)
        data.update(self.wrapper.meta_ext._content)
        utils.write_json(data, jsonFile)
