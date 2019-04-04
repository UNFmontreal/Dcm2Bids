# -*- coding: utf-8 -*-


from collections import OrderedDict
from future.utils import iteritems
from os.path import join as opj
from .utils import DEFAULT
from .version import __version__


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
            return opj(self.name, self.session)
        else:
            return self.name


    @property
    def prefix(self):
        """ The prefix to build filenames

        Returns:
            A string 'sub-<subject_label>' or
            'sub-<subject_label>_ses-<session_label>'
        """
        if self.hasSession():
            return self.name + "_" + self.session
        else:
            return self.name


    def hasSession(self):
        """ Check if a session is set

        Returns:
            Boolean
        """
        return not self.session.strip() == DEFAULT.session



class Acquisition(object):
    """ Class representing an acquisition

    Args:
        participant (Participant): A participant object
        dataType (str): A functional group of MRI data (ex: func, anat ...)
        modalityLabel (str): The modality of the acquisition
                (ex: T1w, T2w, bold ...)
        customLabels (str): Optional labels (ex: task-rest)
        srcSidecar (Sidecar): Optional sidecar object
    """

    def __init__(self, participant, dataType, modalityLabel, customLabels="",
            srcSidecar=None, sidecarChanges={},
            intendedFor=None, IntendedFor=None, **kwargs):
        self._modalityLabel = ""
        self._customLabels = ""
        self._intendedFor = None

        self.participant = participant
        self.dataType = dataType
        self.modalityLabel = modalityLabel
        self.customLabels = customLabels
        self.srcSidecar = srcSidecar
        self.sidecarChanges = sidecarChanges
        if intendedFor is None:
            self.intendedFor = IntendedFor
        else:
            self.intendedFor = intendedFor


    def __eq__(self, other):
        return (
                self.dataType == other.dataType
                and self.participant.prefix == other.participant.prefix
                and self.suffix == other.suffix
                )


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
        self._modalityLabel = self.prepend(modalityLabel)


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
        self._customLabels = self.prepend(customLabels)


    @property
    def suffix(self):
        """ The suffix to build filenames

        Returns:
            A string '_<modalityLabel>' or '_<customLabels>_<modalityLabel>'
        """
        if self.customLabels.strip() == "":
            return self.modalityLabel
        else:
            return self.customLabels + self.modalityLabel


    @property
    def srcRoot(self):
        """
        Return:
            The sidecar source root to move
        """
        if self.srcSidecar:
            return self.srcSidecar.root
        else:
            return None


    @property
    def dstRoot(self):
        """
        Return:
            The destination root inside the BIDS structure
        """
        return opj(
                self.participant.directory,
                self.dataType,
                self.participant.prefix + self.suffix
                )


    @property
    def intendedFor(self):
        return self._intendedFor


    @intendedFor.setter
    def intendedFor(self, value):
        if isinstance(value, list):
            self._intendedFor = value
        else:
            self._intendedFor = [value,]


    def dstSidecarData(self, descriptions):
        """
        """
        data = self.srcSidecar.origData
        data["Dcm2bidsVersion"] = __version__

        #intendedFor key
        if self.intendedFor != [None]:
            intendedValue = []
            for index in self.intendedFor:
                intendedDesc = descriptions[index]

                dataType = intendedDesc["dataType"]

                niiFile = self.participant.prefix
                niiFile += self.prepend(intendedDesc.get("customLabels", ""))
                niiFile += self.prepend(intendedDesc["modalityLabel"])
                niiFile += ".nii.gz"

                intendedValue.append(
                        opj(dataType, niiFile).replace("\\", "/"))

            if len(intendedValue) == 1:
                data["IntendedFor"] = intendedValue[0]
            else:
                data["IntendedFor"] = intendedValue

        #sidecarChanges
        for key, value in iteritems(self.sidecarChanges):
            data[key] = value

        return data


    @staticmethod
    def prepend(value, char="_"):
        """ Prepend `char` to `value` if necessary

        Args:
            value (str)
            char (str)
        """
        if value.strip() == "":
            return ""

        elif value.startswith(char):
            return value

        else:
            return char + value

