# -*- coding: utf-8 -*-


from subprocess import call
import os
import yaml


def make_directory_tree(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class Batch(object):
    """
    """

    def __init__(self, options, bidsDir, participant):
        self.options = options
        self.bidsDir = bidsDir
        self.participant = participant
        self.files = []
        self.codeDir = os.path.join(os.path.abspath(bidsDir), 'code')
        self.yaml = os.path.join(
                self.codeDir, "{}.yml".format(participant.prefix))


    def add(self, acquisition):
        filename = "{}_{}".format(self.participant.prefix, acquisition.suffix)
        in_dir = os.path.relpath(
                os.path.dirname(acquisition.dicomPath),
                self.codeDir)
        out_dir = os.path.relpath(os.path.join(
                self.bidsDir,
                self.participant.directory,
                acquisition.dataType), self.codeDir)
        self.files.append({
                "filename": filename,
                "in_dir": in_dir,
                "out_dir": out_dir,
                })


    def write(self):
        make_directory_tree(self.codeDir)
        data = {"Options": self.options, "Files": self.files}
        with open(self.yaml, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, indent=4)


    def show(self):
        with open(self.yaml, 'r') as f:
            print(f.read())


    def execute(self):
        command = "dcm2niibatch {}".format(self.yaml)
        os.chdir(self.codeDir)
        for f in self.files:
            make_directory_tree(f["out_dir"])
        call(command, shell=True)

