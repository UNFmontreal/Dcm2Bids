# -*- coding: utf-8 -*-


from os.path import join as opj
from .utils import DEFAULT


class Participant(object):
    """ Class representing a participant

    Args:
        name (str): Label of your participant
        session (str): Optional label of a session
    """

    def __init__(self, name, session=DEFAULT.session):
        self._name = ""
        self._session = ""

        self.name = name
        self.session = session


    @property
    def name(self):
        """
        Returns:
            A string 'sub-<subject_label>'
        """
        return self._name


    @name.setter
    def name(self, name):
        """ Prepend 'sub-' if necessary"""
        if name.startswith("sub-"):
            self._name = name

        else:
            self._name = "sub-" + name


    @property
    def session(self):
        """
        Returns:
            A string 'ses-<session_label>'
        """
        return self._session


    @session.setter
    def session(self, session):
        """ Prepend 'ses-' if necessary"""
        if session.strip() == "":
            self._session = ""

        elif session.startswith("ses-"):
            self._session = session

        else:
            self._session = "ses-" + session


    @property
    def directory(self):
        """ The directory of the participant

        Returns:
            A path 'sub-<subject_label>' or
            'sub-<subject_label>/ses-<session_label>'
        """
        if self.hasSession():
            return opj(self._name, self._session)
        else:
            return self._name


    @property
    def prefix(self):
        """ The prefix to build filenames

        Returns:
            A string 'sub-<subject_label>' or
            'sub-<subject_label>_ses-<session_label>'
        """
        if self.hasSession():
            return self._name + "_" + self._session
        else:
            return self._name


    def hasSession(self):
        """ Check if a session is set

        Returns:
            Boolean
        """
        return not self._session.strip() == DEFAULT.session



class Acquisition(object):
    """ Class representing an acquisition

    Args:
        srcRoot (str): The path root (without the extension) of the acquisition
                that is return by dcm2niix
        participant (Participant): A participant object
        dataType (str): A functional group of MRI data (ex: func, anat ...)
        modalityLabel (str): The modality of the acquisition
                (ex: T1w, T2w, bold ...)
        customLabels (str): Optional labels (ex: task-rest)
    """

    def __init__(self, srcRoot, participant,
                 dataType, modalityLabel, customLabels=""):
        self._modalityLabel = ""
        self._customLabels = ""

        self.srcRoot = srcRoot
        self.participant = participant
        self.dataType = dataType
        self.modalityLabel = modalityLabel
        self.customLabels = customLabels


    @property
    def modalityLabel(self):
        """
        Returns:
            A string '_<modalityLabel>'
        """
        return self._modalityLabel


    @modalityLabel.setter
    def modalityLabel(self, modalityLabel):
        """ Prepend '_' if necessary"""
        if modalityLabel.startswith("_"):
            self._modalityLabel = modalityLabel

        else:
            self._modalityLabel = "_" + modalityLabel


    @property
    def customLabels(self):
        """
        Returns:
            A string '_<customLabels>'
        """
        return self._customLabels


    @customLabels.setter
    def customLabels(self, customLabels):
        """ Prepend '_' if necessary"""
        if customLabels.strip() == "":
            self._customLabels = ""

        elif customLabels.startswith("_"):
            self._customLabels = customLabels

        else:
            self._customLabels = "_" + customLabels


    @property
    def suffix(self):
        """ The suffix to build filenames

        Returns:
            A string '_<modalityLabel>' or '_<customLabels>_<modalityLabel>'
        """
        if self._customLabels.strip() == "":
            return self._modalityLabel
        else:
            return self._customLabels + self._modalityLabel


    def get_src_path(self, extension):
        """ Build a source path from srcRoot

        Args:
            extension (str): extension of the file

        Return:
            A path to a source file with the extension specified
        """
        if not extension.startswith("."):
            extension = "." + extension

        return self.srcRoot + extension


    def get_dst_path(self, extension):
        """ Build a destination path

        Args:
            extension (str): extension of the file

        Return:
            A path to a destination file with the extension specified
        """
        if not extension.startswith("."):
            extension = "." + extension

        return opj(
                self.participant.directory,
                self.dataType,
                self.participant.prefix + self.suffix + extension
                )

