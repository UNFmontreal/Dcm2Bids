# -*- coding: utf-8 -*-

"""sidecars classes"""

import itertools
import logging
import os
import re
from collections import defaultdict, OrderedDict
from fnmatch import fnmatch

from dcm2bids.acquisition import Acquisition
from dcm2bids.utils.io import load_json
from dcm2bids.utils.utils import (DEFAULT, convert_dir, combine_dict_extractors,
                                  splitext_)

compare_float_keys = ["lt", "gt", "le", "ge", "btw", "btwe"]


class Sidecar(object):
    """ A sidecar object

    Args:
        filename (str): Path of a JSON sidecar
        keyComp (list): A list of keys from the JSON sidecar to compare sidecars
                     default=["SeriesNumber","AcquisitionTime","SideCarFilename"]
    """

    def __init__(self, filename, compKeys=DEFAULT.compKeys):
        self._origData = {}
        self._data = {}
        self.filename = filename
        self.root, _ = splitext_(filename)
        self.data = filename
        self.compKeys = compKeys

    def __lt__(self, other):
        lts = []
        for key in self.compKeys:
            try:
                if all(key in d for d in (self.data, other.data)):
                    if self.data.get(key) == other.data.get(key):
                        lts.append(None)
                    else:
                        lts.append(self.data.get(key) < other.data.get(key))
                else:
                    lts.append(None)

            except Exception:
                lts.append(None)

        for lt in lts:
            if lt is not None:
                return lt

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return hash(self.filename)

    @property
    def origData(self):
        return self._origData

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, filename):
        """
        Args:
            filename (path): path of a JSON file

        Return:
            A dictionary of the JSON content plus the SidecarFilename
        """
        try:
            data = load_json(filename)
        except Exception:
            data = {}
        self._origData = data.copy()
        data["SidecarFilename"] = os.path.basename(filename)
        self._data = data


class SidecarPairing(object):
    """
    Args:
        sidecars (list): List of Sidecar objects
        descriptions (list): List of dictionaries describing acquisitions
    """

    def __init__(self,
                 sidecars,
                 descriptions,
                 extractors=DEFAULT.extractors,
                 auto_extractor=DEFAULT.auto_extract_entities,
                 do_not_reorder_entities=DEFAULT.do_not_reorder_entities,
                 search_method=DEFAULT.search_method,
                 case_sensitive=DEFAULT.case_sensitive,
                 dup_method=DEFAULT.dup_method,
                 post_op=DEFAULT.post_op,
                 bids_uri=DEFAULT.bids_uri):
        self.logger = logging.getLogger(__name__)
        self._search_method = ""
        self._dup_method = ""
        self._post_op = ""
        self._bids_uri = ""
        self.graph = OrderedDict()
        self.acquisitions = []
        self.extractors = extractors
        self.auto_extract_entities = auto_extractor
        self.do_not_reorder_entities = do_not_reorder_entities
        self.sidecars = sidecars
        self.descriptions = descriptions
        self.search_method = search_method
        self.case_sensitive = case_sensitive
        self.dup_method = dup_method
        self.post_op = post_op
        self.bids_uri = bids_uri

    @property
    def search_method(self):
        return self._search_method

    @search_method.setter
    def search_method(self, value):
        """
        Checks if the search method is implemented
        Warns the user if not and fall back to default
        """
        if value in DEFAULT.search_methodChoices:
            self._search_method = value

        else:
            self._search_method = DEFAULT.search_method
            self.logger.warning(f"'{value}' is not a search method implemented")
            self.logger.warning(f"Falling back to default: {DEFAULT.search_method}")
            self.logger.warning(
                f"Search methods implemented: {DEFAULT.search_methodChoices}"
            )

    @property
    def dup_method(self):
        return self._dup_method

    @dup_method.setter
    def dup_method(self, value):
        """
        Checks if the duplicate method is implemented
        Warns the user if not and fall back to default
        """
        if value in DEFAULT.dup_method_choices:
            self._dup_method = value
        else:
            self._dup_method = DEFAULT.dup_method
            self.logger.warning(
                "Duplicate methods implemented: %s", DEFAULT.dup_method_choices)
            self.logger.warning(f"{value} is not a duplicate method implemented.")
            self.logger.warning(f"Falling back to default: {DEFAULT.dup_method}.")

    @property
    def post_op(self):
        return self._post_op

    @post_op.setter
    def post_op(self, value):
        """
        Checks if post_op commands don't overlap
        """
        post_op = []
        if isinstance(value, dict):
            value = [value]
        elif not isinstance(value, list):
            raise ValueError("post_op should be a list of dict."
                             "Please check the documentation.")

        try:
            pairs = []
            for curr_post_op in value:
                post_op.append(curr_post_op)
                datatype = curr_post_op['datatype']
                suffix = curr_post_op['suffix']

                if 'custom_entities' in curr_post_op:
                    post_op[-1]['custom_entities'] = curr_post_op['custom_entities']

                if isinstance(curr_post_op['cmd'], str):
                    cmd_split = curr_post_op['cmd'].split()
                else:
                    raise ValueError("post_op cmd should be a string."
                                     "Please check the documentation.")

                if 'src_file' not in cmd_split or 'dst_file' not in cmd_split:
                    raise ValueError("post_op cmd is not defined correctly. "
                                     "<src_file> and/or <dst_file> is missing. "
                                     "Please check the documentation.")

                if isinstance(datatype, str):
                    post_op[-1]['datatype'] = [datatype]
                    datatype = [datatype]

                if isinstance(suffix, str):
                    # It will be compare with acq.suffix which has a `_` character
                    post_op[-1]['suffix'] = ['_' + suffix]
                    suffix = [suffix]
                elif isinstance(suffix, list):
                    post_op[-1]['suffix'] = ['_' + curr_suffix for curr_suffix in suffix]

                pairs = pairs + list(itertools.product(datatype, suffix))

            res = list(set([ele for ele in pairs if pairs.count(ele) > 1]))
            if res:
                raise ValueError("Some post operations apply on "
                                 "the same combination of datatype/suffix. "
                                 "Please fix post_op key in your config file."
                                 f"{pairs}")

            self._post_op = post_op

        except Exception:
            raise ValueError("post_op is not defined correctly. "
                             "Please check the documentation.")

    @property
    def bids_uri(self):
        return self._bids_uri

    @bids_uri.setter
    def bids_uri(self, value):
        """
        Checks if the method bids_uri is using is implemented
        Warns the user if not and fall back to default
        """
        if value in DEFAULT.bids_uri_choices:
            self._bids_uri = value
        else:
            self.bids_uri = DEFAULT.bids_uri
            self.logger.warning(
                "BIDS URI methods implemented: %s", DEFAULT.bids_uri_choices)
            self.logger.warning(f"{value} is not a bids URI method implemented.")
            self.logger.warning(f"Falling back to default: {DEFAULT.bids_uri}.")

    @property
    def case_sensitive(self):
        return self._case_sensitive

    @case_sensitive.setter
    def case_sensitive(self, value):
        if isinstance(value, bool):
            self._case_sensitive = value
        else:
            self._case_sensitive = DEFAULT.case_sensitive
            self.logger.warning(f"'{value}' is not a boolean")
            self.logger.warning(f"Falling back to default: {DEFAULT.case_sensitive}")
            self.logger.warning(f"Search methods implemented: {DEFAULT.case_sensitive}")

    def build_graph(self):
        """
        Test all the possible links between the list of sidecars and the
        description dictionaries and build a graph from it
        The graph is in a OrderedDict object. The keys are the Sidecars and
        the values are a list of possible descriptions

        Returns:
            A graph (OrderedDict)
        """
        graph = OrderedDict((_, []) for _ in self.sidecars)
        possibleLinks = itertools.product(self.sidecars, self.descriptions)
        for sidecar, description in possibleLinks:
            criteria = description.get("criteria", None)
            if criteria and self.isLink(sidecar.data, criteria):
                graph[sidecar].append(description)

        self.graph = graph

        return graph

    def isLink(self, data, criteria):
        """
        Args:
            data (dict): Dictionary data of a sidecar
            criteria (dict): Dictionary criteria

        Returns:
            boolean
        """

        def compare(name, pattern):
            name = str(name)
            if self.search_method == "re":
                return bool(re.match(pattern, name))
            else:
                pattern = str(pattern)
                if not self.case_sensitive:
                    name = name.lower()
                    pattern = pattern.lower()

                return fnmatch(name, pattern)

        def compare_list(name, pattern):
            try:
                subResult = [
                        len(name) == len(pattern),
                        isinstance(pattern, list),
                        ]
                for subName, subPattern in zip(name, pattern):
                    subResult.append(compare(subName, subPattern))
            except Exception:
                subResult = [False]
            return all(subResult)

        def compare_complex(name, pattern):
            sub_result = []
            compare_type = None
            try:
                for compare_type, patterns in pattern.items():
                    for sub_pattern in patterns:
                        if isinstance(name, list):
                            sub_result.append(compare_list(name, sub_pattern))
                        else:
                            sub_result.append(compare(name, sub_pattern))
            except Exception:
                sub_result = [False]

            if compare_type == "any":
                return any(sub_result)
            else:
                return False

        def compare_float(name, pattern):
            try:
                comparison = list(pattern.keys())[0]
                name_float = float(name)

                sub_pattern = pattern[list(pattern.keys())[0]]

                if comparison in ["btwe", "btw"]:
                    if not isinstance(sub_pattern, list):
                        raise ValueError("You should be using a list "
                                         "for float comparison "
                                         f"with key {comparison}. "
                                         f"Error val: {sub_pattern}")

                    if len(sub_pattern) != 2:
                        raise ValueError(f"List for key {comparison} "
                                         "should have two values. "
                                         f"Error val: {sub_pattern}")

                    elif comparison == "btwe":
                        return name_float >= float(sub_pattern[0]) and name_float <= float(sub_pattern[1])
                    elif comparison == "btw":
                        return name_float > float(sub_pattern[0]) and name_float < float(sub_pattern[1])

                if isinstance(sub_pattern, list):
                    if len(sub_pattern) != 1:
                        raise ValueError(f"List for key {comparison} "
                                         "should have only one value. "
                                         "Error val: {sub_pattern}")

                    sub_pattern = float(sub_pattern[0])
                else:
                    sub_pattern = float(sub_pattern)

                if comparison == 'gt':
                    return sub_pattern < name_float
                elif comparison == 'lt':
                    return sub_pattern > name_float
                elif comparison == 'ge':
                    return sub_pattern <= name_float
                elif comparison == 'le':
                    return sub_pattern >= name_float

            except Exception:
                return False

        result = []

        for tag, pattern in criteria.items():
            name = data.get(tag, '')

            if isinstance(pattern, dict):
                if len(pattern.keys()) == 1:
                    if "any" in pattern.keys():
                        result.append(compare_complex(name, pattern))
                    elif list(pattern.keys())[0] in compare_float_keys:
                        result.append(compare_float(name, pattern))
                    else:
                        self.logger.warning(f"This key {list(pattern.keys())[0]} "
                                            "is not allowed.")
                else:
                    raise ValueError("Dictionary used as criteria should be "
                                     "using only one key.")

            elif isinstance(name, list):
                result.append(compare_list(name, pattern))
            else:
                result.append(compare(name, pattern))

        return all(result)

    def build_acquisitions(self, participant):
        """
        Args:
            participant (Participant): Participant object to create acquisitions
        Returns:
            A list of acquisition objects
        """
        acquisitions_id = []
        acquisitions = []
        self.logger.info("Sidecar pairing".upper())
        for sidecar, valid_descriptions in self.graph.items():
            sidecarName = os.path.basename(sidecar.root)

            # only one description for the sidecar
            if len(valid_descriptions) == 1:
                desc = valid_descriptions[0]
                desc, sidecar = self.searchDcmTagEntity(sidecar, desc)
                acq = Acquisition(participant,
                                  src_sidecar=sidecar,
                                  bids_uri=self.bids_uri,
                                  do_not_reorder_entities=self.do_not_reorder_entities,
                                  **desc)
                acq.setDstFile()

                if acq.id:
                    acquisitions_id.append(acq)
                else:
                    acquisitions.append(acq)

                self.logger.info(
                  f"{acq.dstFile.replace(f'{acq.participant.prefix}-', '')}"
                  f"  <-  {sidecarName}")

            elif len(valid_descriptions) == 0:
                self.logger.info(f"No Pairing  <-  {sidecarName}")

            else:
                self.logger.warning(f"Several Pairing  <-  {sidecarName}")
                for desc in valid_descriptions:
                    acq = Acquisition(participant,
                                      bids_uri=self.bids_uri,
                                      do_not_reorder_entities=self.do_not_reorder_entities,
                                      **desc)
                    self.logger.warning(f"    ->  {acq.suffix}")

        self.acquisitions = acquisitions_id + acquisitions

        return self.acquisitions

    def searchDcmTagEntity(self, sidecar, desc):
        """
        Add DCM Tag to custom_entities
        """
        descWithTask = desc.copy()
        concatenated_matches = {}
        keys_custom_entities = []
        entities = []
        if "custom_entities" in desc.keys() or self.auto_extract_entities:
            if 'custom_entities' in desc.keys():
                if isinstance(descWithTask["custom_entities"], str):
                    descWithTask["custom_entities"] = [descWithTask["custom_entities"]]
            else:
                descWithTask["custom_entities"] = []

            keys_custom_entities = [curr_entity.split('-')[0] for curr_entity in descWithTask["custom_entities"]]

            if self.auto_extract_entities:
                self.extractors = combine_dict_extractors(self.extractors, DEFAULT.auto_extractors)

            # Loop to check if we find self.extractor
            for dcmTag in self.extractors:
                if dcmTag in sidecar.data.keys():
                    dcmInfo = sidecar.data.get(dcmTag)
                    for regex in self.extractors[dcmTag]:
                        compile_regex = re.compile(regex)
                        if not isinstance(dcmInfo, list):
                            if compile_regex.search(str(dcmInfo)) is not None:
                                concatenated_matches.update(
                                    compile_regex.search(str(dcmInfo)).groupdict())
                        else:
                            for curr_dcmInfo in dcmInfo:
                                if compile_regex.search(curr_dcmInfo) is not None:
                                    concatenated_matches.update(
                                        compile_regex.search(curr_dcmInfo).groupdict())
                                    break

            # Keep entities asked in custom_entities
            # If dir found in custom_entities and concatenated_matches.keys we keep it
            if "custom_entities" in desc.keys() and not self.auto_extract_entities:
                entities = desc["custom_entities"]
            elif "custom_entities" in desc.keys():
                entities = set(concatenated_matches.keys()).intersection(set(descWithTask["custom_entities"]))

                # custom_entities not a key for extractor or auto_extract_entities
                complete_entities = [ent for ent in descWithTask["custom_entities"] if '-' in ent]
                entities = entities.union(set(complete_entities))
            if self.auto_extract_entities:
                auto_acq = '_'.join([descWithTask['datatype'], descWithTask["suffix"]])
                if auto_acq in DEFAULT.auto_entities:
                    # Check if these auto entities have been found before merging
                    auto_entities = set(concatenated_matches.keys()).intersection(set(DEFAULT.auto_entities[auto_acq]))

                    left_auto_entities = auto_entities.symmetric_difference(set(DEFAULT.auto_entities[auto_acq]))
                    left_auto_entities = left_auto_entities.difference(keys_custom_entities)

                    if left_auto_entities:
                        self.logger.warning(f"Entities {left_auto_entities} have not been found "
                                            f"for datatype '{descWithTask['datatype']}' "
                                            f"and suffix '{descWithTask['suffix']}'.")

                    entities = list(entities) + list(auto_entities)
                    entities = list(set(entities))
                    descWithTask["custom_entities"] = entities

            for curr_entity in entities:
                if curr_entity in concatenated_matches.keys():
                    if curr_entity == 'dir':
                        descWithTask["custom_entities"] = list(map(lambda x: x.replace(curr_entity, '-'.join([curr_entity, convert_dir(concatenated_matches[curr_entity])])), descWithTask["custom_entities"]))
                    elif curr_entity == 'task':
                        sidecar.data['TaskName'] = concatenated_matches[curr_entity]
                        descWithTask["custom_entities"] = list(map(lambda x: x.replace(curr_entity, '-'.join([curr_entity, concatenated_matches[curr_entity]])), descWithTask["custom_entities"]))
                    else:
                        descWithTask["custom_entities"] = list(map(lambda x: x.replace(curr_entity, '-'.join([curr_entity, concatenated_matches[curr_entity]])), descWithTask["custom_entities"]))

            # Remove entities without -
            for curr_entity in descWithTask["custom_entities"]:
                if '-' not in curr_entity:
                    self.logger.info(f"Removing entity '{curr_entity}' since it "
                                     "does not fit the basic BIDS specification "
                                     "(Entity-Value)")
                    descWithTask["custom_entities"].remove(curr_entity)

        return descWithTask, sidecar

    def find_runs(self):
        """
        Check if there is duplicate destination roots in the acquisitions
        and add '_run-' to the custom_entities of the acquisition
        """

        def duplicates(seq):
            """ Find duplicate items in a list

            Args:
                seq (list)

            Yield:
                A tuple of 2 items (item, list of index)

            ref: http://stackoverflow.com/a/5419576
            """
            tally = defaultdict(list)
            for i, item in enumerate(seq):
                tally[item].append(i)

            for key, locs in tally.items():
                if len(locs) > 1:
                    yield key, locs

        dstRoots = [_.dstRoot for _ in self.acquisitions]

        templateDup = DEFAULT.runTpl
        if self.dup_method == 'dup':
            templateDup = DEFAULT.dupTpl

        for dstRoot, dup in duplicates(dstRoots):
            self.logger.info(f"{dstRoot} has {len(dup)} runs")
            self.logger.info(f"Adding {self.dup_method} information to the acquisition")
            if self.dup_method == 'dup':
                dup = dup[0:-1]

            for runNum, acqInd in enumerate(dup):
                runStr = templateDup.format(runNum+1)
                self.acquisitions[acqInd].custom_entities += runStr
                self.acquisitions[acqInd].setDstFile()
