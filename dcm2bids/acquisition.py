# -*- coding: utf-8 -*-

"""Participant class"""

import logging
from os.path import join as opj
from os import sep

from dcm2bids.utils.utils import DEFAULT
from dcm2bids.version import __version__


class Acquisition(object):
    """ Class representing an acquisition

    Args:
        participant (Participant): A participant object
        datatype (str): A functional group of MRI data (ex: func, anat ...)
        suffix (str): The modality of the acquisition
                (ex: T1w, T2w, bold ...)
        custom_entities (str): Optional entities (ex: task-rest)
        src_sidecar (Sidecar): Optional sidecar object
    """

    def __init__(
        self,
        participant,
        datatype,
        suffix,
        custom_entities="",
        id=None,
        src_sidecar=None,
        sidecar_changes=None,
        bids_uri=None,
        do_not_reorder_entities=None,
        **kwargs
    ):
        self.logger = logging.getLogger(__name__)

        self._suffix = ""
        self._custom_entities = ""
        self._id = ""

        self.participant = participant
        self.datatype = datatype
        self.suffix = suffix
        self.custom_entities = custom_entities
        self.src_sidecar = src_sidecar
        self.bids_uri = bids_uri
        self.do_not_reorder_entities = do_not_reorder_entities

        if sidecar_changes is None:
            self.sidecar_changes = {}
        else:
            self.sidecar_changes = sidecar_changes

        if id is None:
            self.id = None
        else:
            self.id = id

        self.dstFile = ''
        self.extraDstFile = ''

    def __eq__(self, other):
        return (
            self.datatype == other.datatype
            and self.participant.prefix == other.participant.prefix
            and self.build_suffix == other.build_suffix
        )

    @property
    def suffix(self):
        """
        Returns:
            A string '_<suffix>'
        """
        return self._suffix

    @suffix.setter
    def suffix(self, suffix):
        """ Prepend '_' if necessary"""
        self._suffix = self.prepend(suffix)

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
    def custom_entities(self):
        """
        Returns:
            A string '_<custom_entities>'
        """
        return self._custom_entities

    @custom_entities.setter
    def custom_entities(self, custom_entities):
        """ Prepend '_' if necessary"""
        if isinstance(custom_entities, list):
            self._custom_entities = self.prepend('_'.join(custom_entities))
        else:
            self._custom_entities = self.prepend(custom_entities)

    @property
    def build_suffix(self):
        """ The suffix to build filenames

        Returns:
            A string '_<suffix>' or '_<custom_entities>_<suffix>'
        """
        if self.custom_entities.strip() == "":
            return self.suffix
        else:
            return self.custom_entities + self.suffix

    @property
    def srcRoot(self):
        """
        Return:
            The sidecar source root to move
        """
        if self.src_sidecar:
            return self.src_sidecar.root
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
            self.datatype,
            self.dstFile,
        )

    @property
    def dstId(self):
        """
        Return:
            The destination root inside the BIDS structure for description
        """
        return opj(
            self.participant.session,
            self.datatype,
            self.dstFile,
        )

    def setExtraDstFile(self, new_entities):
        """
        Return:
            The destination filename formatted following
            the v1.9.0 BIDS entity key table
            https://bids-specification.readthedocs.io/en/v1.9.0/99-appendices/04-entity-table.html
        """

        if self.custom_entities.strip() == "":
            suffix = new_entities + self.suffix
        elif isinstance(new_entities, list):
            suffix = '_'.join(new_entities) + self.custom_entities + self.suffix
        elif isinstance(new_entities, str):
            suffix = new_entities + self.custom_entities + self.suffix

        current_name = '_'.join([self.participant.prefix, suffix])

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
            self.logger.warning(f'Entity \"{list(current_dict.keys())}\"'
                                ' is not a valid BIDS entity.')

        # Allow multiple single keys (without value)
        new_name += f"_{'_'.join(suffix_list)}"

        if len(suffix_list) != 1:
            self.logger.warning("There was more than one suffix found "
                                f"({suffix_list}). This is not BIDS "
                                "compliant. Make sure you know what "
                                "you are doing.")

        if not self.do_not_reorder_entities:
            if current_name != new_name:
                self.logger.warning(
                    f"""✅ Filename was reordered according to BIDS entity table order:
                    from:   {current_name}
                    to:     {new_name}""")
        else:
            new_name = current_name

        self.extraDstFile = opj(self.participant.directory,
                                self.datatype,
                                new_name)

    def setDstFile(self):
        """
        Return:
            The destination filename formatted following
            the v1.9.0 BIDS entity key table
            https://bids-specification.readthedocs.io/en/v1.9.0/99-appendices/04-entity-table.html
        """
        current_name = self.participant.prefix + self.build_suffix
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
            self.logger.warning(f'Entity \"{list(current_dict.keys())}\"'
                                ' is not a valid BIDS entity.')

        # Allow multiple single keys (without value)
        new_name += f"_{'_'.join(suffix_list)}"

        if len(suffix_list) != 1:
            self.logger.warning("There was more than one suffix found "
                                f"({suffix_list}). This is not BIDS "
                                "compliant. Make sure you know what "
                                "you are doing.")

        self.dstFile = current_name
        if not self.do_not_reorder_entities:
            if current_name != new_name:
                self.logger.warning(
                    f"""✅ Filename was reordered according to BIDS entity table order:
                    from:   {current_name}
                    to:     {new_name}""")
                self.dstFile = new_name


    def dstSidecarData(self, idList):
        """
        """
        data = self.src_sidecar.origData
        data["Dcm2bidsVersion"] = __version__

        # TaskName
        if 'TaskName' in self.src_sidecar.data:
            data["TaskName"] = self.src_sidecar.data["TaskName"]

        # sidecar_changes
        for key, value in self.sidecar_changes.items():
            values = []

            if not isinstance(value, list):
                value = [value]

            for val in value:
                if isinstance(val, (bool, str, int, float)):
                    if val not in idList and key in DEFAULT.keyWithPathsidecar_changes:
                        logging.warning(f"No id found for '{key}' value '{val}'.")
                        logging.warning(f"No sidecar changes for field '{key}' "
                                        f"will be made "
                                        f"for json file '{self.dstFile}.json' "
                                        "with this id.")
                    else:
                        values.append(idList.get(val, val))
                        if values[-1] != val:
                            if self.bids_uri == DEFAULT.bids_uri:
                                if isinstance(values[-1], list):
                                    values[-1] = ["bids::" + img_dest for img_dest in values[-1]]
                                else:
                                    values[-1] = "bids::" + values[-1]
                            else:
                                if isinstance(values[-1], list):
                                    values[-1] = [img_dest.replace(self.participant.name + sep, "") for img_dest in values[-1]]
                                else:
                                    values[-1] = values[-1].replace(self.participant.name + sep, "")

            # handle if nested list vs str
            flat_value_list = []
            for item in values:
                if isinstance(item, list):
                    flat_value_list += item
                else:
                    flat_value_list.append(item)

            if len(flat_value_list) == 1:
                data[key] = flat_value_list[0]
            else:
                data[key] = flat_value_list

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
