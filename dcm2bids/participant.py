# -*- coding: utf-8 -*-


class Participant(object):
    """
    """

    def __init__(self, name):
        self.name = "sub-{}".format(name)


    def getName(self):
        return self.name
