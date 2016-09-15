# -*- coding: utf-8 -*-


from subprocess import call
import utils
import os


class Batch(object):
    """
    """

    def __init__(self, codeDir, session):
        self._codeDir = codeDir
        self._session = session
        self._yamlName = "{}.yaml".format(self._session.prefix)
        self._cmdTemplate = 'dcm2niibatch {}'
        self._yamlFile = os.path.join(self._codeDir, self._yamlName)
        self._options = {
                "isGz": True,
                "isFlipY": False,
                "isVerbose": False,
                "isCreateBIDS": True,
                "isOnlySingleFile": False,
                }
        self._files = []

    @property
    def data(self):
        return {"Options": self._options, "Files": self._files}

    @property
    def command(self):
        return self._cmdTemplate.format(self._yamlName)

    def add(self, acq):
        utils.make_directory_tree(acq.outDir)
        self._files.append({
                "filename": acq.filename,
                "in_dir": os.path.relpath(acq.inDir, self._codeDir),
                "out_dir": os.path.relpath(acq.outDir, self._codeDir),
                })

    def write(self):
        utils.write_yaml(self.data, self._yamlFile)

    def show(self):
        with open(self._yamlFile, 'r') as f:
            utils.info(f.read())

    def launch(self):
        os.chdir(self._codeDir)
        call(self.command, shell=True)
