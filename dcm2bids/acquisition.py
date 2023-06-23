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
        customEntities (str): Optional entities (ex: task-rest)
        srcSidecar (Sidecar): Optional sidecar object
    """

    def __init__(
        self,
        participant,
        dataType,
        modalityLabel,
        customEntities="",
        id=None,
        srcSidecar=None,
        sidecarChanges=None,
        intendedFor=None,
        IntendedFor=None,
        **kwargs
    ):
        self.logger = logging.getLogger(__name__)

        self._modalityLabel = ""
        self._customEntities = ""
        self._id = ""
        self._intendedFor = None

        self.participant = participant
        self.dataType = dataType
        self.modalityLabel = modalityLabel
        self.customEntities = customEntities
        self.srcSidecar = srcSidecar
        self.sidecarChanges = {} if sidecarChanges is None else sidecarChanges
        self.intendedFor = IntendedFor if intendedFor is None else intendedFor
        self.id = None if id is None else id
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
    def id(self):
        """
        Returns:
            A string '_<id>'
        """
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def customEntities(self):
        """
        Returns:
            A string '_<customEntities>'
        """
        return self._customEntities

    @customEntities.setter
    def customEntities(self, customEntities):
        """ Prepend '_' if necessary"""
        if isinstance(customEntities, list):
            self._customEntities = self.prepend('_'.join(customEntities))
        else:
            self._customEntities = self.prepend(customEntities)

    @property
    def suffix(self):
        """ The suffix to build filenames

        Returns:
            A string '_<modalityLabel>' or '_<customEntities>_<modalityLabel>'
        """
        if self.customEntities.strip() == "":
            return self.modalityLabel
        else:
            return self.customEntities + self.modalityLabel

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
            The destination filename formatted following the v1.8.0
            BIDS entity key table
            https://bids-specification.readthedocs.io/en/v1.8.0/99-appendices/04-entity-table.html
        """
        current_name = self.participant.prefix + self.suffix
        new_name = ''
        current_dict = dict(
          x.split("-") for x in current_name.split("_") if len(x.split('-')) == 2
          )
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
            self.logger.warning(f"Entity \"{list(current_dict.keys())}\" is"
                                "not a valid BIDS entity.")

        # Allow multiple single keys (without value)
        new_name += f"_{'_'.join(suffix_list)}"

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

    def dstSidecarData(self, intendedForList):
        """
        """
        data = self.srcSidecar.origData
        data["Dcm2bidsVersion"] = __version__

        # TaskName
        if 'TaskName' in self.srcSidecar.data:
            data["TaskName"] = self.srcSidecar.data["TaskName"]

        # intendedFor key
        if self.intendedFor != [None]:
            intendedValue = []

            for index in self.intendedFor:
                if index in intendedForList:
                    intendedValue = intendedValue + [intendedForList[index]]
                else:
                    logging.warning(f"No id found for IntendedFor value '{index}'.")
                    logging.warning(f"No sidecar changes for field IntendedFor"
                                    f"will be made "
                                    f"for json file {self.dstFile}.json with this id.")
                    logging.warning("Check: https://unfmontreal.github.io/Dcm2Bids/docs/how-to/create-config-file/#id-and-intendedFor.\n")

            data["IntendedFor"] = [
                item for sublist in intendedValue for item in sublist
            ]
        # sidecarChanges
        for key, value in self.sidecarChanges.items():
            if key == "Sources":
                values = [intendedForList.get(val, val) for val in value]
                # handle if nested list vs str
                flat_value_list = []
                for item in values:
                    if isinstance(item, list):
                        flat_value_list += item
                    else:
                        flat_value_list.append(item)
                data[key] = flat_value_list
            else:
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
