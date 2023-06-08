# -*- coding: utf-8 -*-

"""Participant class"""

import logging
from os.path import join as opj

from dcm2bids.utils.utils import DEFAULT
from dcm2bids.version import __version__


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

    def __init__(
        self,
        participant,
        dataType,
        modalityLabel,
        indexSidecar=None,
        customLabels="",
        srcSidecar=None,
        sidecarChanges=None,
        intendedFor=None,
        IntendedFor=None,
        **kwargs
    ):
        self.logger = logging.getLogger(__name__)

        self._modalityLabel = ""
        self._customLabels = ""
        self._intendedFor = None
        self._indexSidecar = None

        self.participant = participant
        self.dataType = dataType
        self.modalityLabel = modalityLabel
        self.customLabels = customLabels
        self.srcSidecar = srcSidecar

        if sidecarChanges is None:
            self.sidecarChanges = {}
        else:
            self.sidecarChanges = sidecarChanges

        if intendedFor is None:
            self.intendedFor = IntendedFor
        else:
            self.intendedFor = intendedFor

        self.dstFile = ''

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
            self.dstFile,
        )

    @property
    def dstIntendedFor(self):
        """
        Return:
            The destination root inside the BIDS structure for intendedFor
        """
        return opj(
            self.participant.session,
            self.dataType,
            self.dstFile,
        )

    def setDstFile(self):
        """
        Return:
            The destination filename formatted following the v1.7.0 BIDS entity key table
            https://bids-specification.readthedocs.io/en/v1.7.0/99-appendices/04-entity-table.html
        """
        current_name = self.participant.prefix + self.suffix
        new_name = ''
        current_dict = dict(x.split("-") for x in current_name.split("_") if len(x.split('-')) == 2)
        suffix_list = [x for x in current_name.split("_") if len(x.split('-')) == 1]

        for current_key in DEFAULT.entityTableKeys:
            if current_key in current_dict and new_name != '':
                new_name += f"_{current_key}-{current_dict[current_key]}"
            elif current_key in current_dict:
                new_name = f"{current_key}-{current_dict[current_key]}"
            current_dict.pop(current_key, None)

        for current_key in current_dict:
            new_name += f"_{current_key}-{current_dict[current_key]}"

        if current_dict:
            self.logger.warning("Entity \"{}\"".format(list(current_dict.keys())) +
                                " is not a valid BIDS entity.")

        new_name += f"_{'_'.join(suffix_list)}"  # Allow multiple single keys (without value)

        if len(suffix_list) != 1:
            self.logger.warning("There was more than one suffix found "
                                f"({suffix_list}). This is not BIDS "
                                "compliant. Make sure you know what "
                                "you are doing.")

        if current_name != new_name:
            self.logger.warning(
                f"""✅ Filename was reordered according to BIDS entity table order:
                from:   {current_name}
                to:     {new_name}""")

        self.dstFile = new_name

    @property
    def intendedFor(self):
        return self._intendedFor

    @intendedFor.setter
    def intendedFor(self, value):
        if isinstance(value, list):
            self._intendedFor = value
        else:
            self._intendedFor = [value]

    @property
    def indexSidecar(self):
        """
        Returns:
            A int '_<indexSidecar>'
        """
        return self._indexSidecar

    @indexSidecar.setter
    def indexSidecar(self, value):
        """
        Returns:
            A int '_<indexSidecar>'
        """
        self._indexSidecar = value

    def dstSidecarData(self, descriptions, intendedForList):
        """
        """
        data = self.srcSidecar.origData
        data["Dcm2bidsVersion"] = __version__

        # intendedFor key
        if self.intendedFor != [None]:
            intendedValue = []

            for index in self.intendedFor:
                intendedValue = intendedValue + intendedForList[index]

            if len(intendedValue) == 1:
                data["IntendedFor"] = intendedValue[0]
            else:
                data["IntendedFor"] = intendedValue

        # sidecarChanges
        for key, value in self.sidecarChanges.items():
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
