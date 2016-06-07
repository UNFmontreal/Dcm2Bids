# -*- coding: utf-8 -*-


from dicomparser import Dicomparser
import dcm2bids_utils as utils
import os


class Acquisition(object):
    """
    """


    def __init__(self, description, dicomDir, participant, session):
        self._description = description
        self._dicomDir = dicomDir
        self._participant = participant
        self._session = session


    @property
    def dataType(self):
        return self._description['data_type']


    @property
    def suffix(self):
        result = ''
        if not self._session.isSingle():
            result += '{}_'.format(self._session.name)
        if self._description.has_key('custom_labels'):
            for key, value in self._description['custom_labels'].iteritems():
                result += '{}-{}_'.format(key, value)
        result += self._description['suffix']
        return result


    @property
    def in_dir(self):
        return os.path.join(self._dicomDir, self._description['directory'])


    @property
    def out_dir(self):
        out_dir = os.path.join(self._session.directory, self.dataType)
        utils.make_directory_tree(out_dir)
        return os.path.join(out_dir)


    @property
    def filename(self):
        return '{}_{}'.format(self._participant.name, self.suffix)


    def writeJson(self, out_dir):
        parser = Dicomparser(self._dicomDir)
        filename = '{}.json'.format(self.filename)
        parser.write(self._dicomDir, os.path.join(out_dir, filename))
