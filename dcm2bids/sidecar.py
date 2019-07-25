# -*- coding: utf-8 -*-


import itertools
import logging
import os
import re
from collections import defaultdict, OrderedDict
from fnmatch import fnmatch
from future.utils import iteritems
from .structure import Acquisition
from .utils import DEFAULT, load_json, splitext_, isDictsEqual


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
                lts.append(self.data.get(key) < other.data.get(key))
            except:
                lts.append(False)

        for lt in lts:
            if lt:
                return True
            else:
                pass

        return False


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
            A dictionnary of the JSON content plus the SidecarFilename
        """
        try:
            data = load_json(filename)
        except:
            data = {}
        self._origData = data.copy()
        data["SidecarFilename"] = os.path.basename(filename)
        self._data = data


class SidecarPairing(object):
    """
    Args:
        sidecars (list): List of Sidecar objects
        descriptions (list): List of dictionnaries describing acquisitions
    """

    def __init__(self, sidecars, descriptions,
            searchMethod=DEFAULT.searchMethod,
            dcmTagLabel="",
            dupMethod=DEFAULT.duplicateMethod):
        self.logger = logging.getLogger(__name__)

        self._searchMethod = ""
        self._dcmTagLabel = ""
        self._dupMethod = ""
        self.graph = OrderedDict()
        self.aquisitions = []
        self.dstImage = [[] for i in itertools.repeat(None, len(descriptions))]

        self.sidecars = sidecars
        self.descriptions = descriptions
        self.searchMethod = searchMethod
        self.dcmTagLabel = dcmTagLabel
        self.dupMethod = dupMethod


    @property
    def searchMethod(self):
        return self._searchMethod

    @property
    def dcmTagLabel(self):
        return self._dcmTagLabel

    @dcmTagLabel.setter
    def dcmTagLabel(self, value):
        self._dcmTagLabel = value

    @property
    def dupMethod(self):
        return self._dupMethod

    @searchMethod.setter
    def searchMethod(self, value):
        """
        Checks if the search method is implemented
        Warns the user if not and fall back to default
        """
        if value in DEFAULT.searchMethodChoices:
            self._searchMethod = value

        else:
            self._searchMethod = DEFAULT.searchMethod
            self.logger.warning(
                    "'{}' is not a search method implemented".format(value))
            self.logger.warning(
                    "Falling back to default: {}".format(DEFAULT.searchMethod))
            self.logger.warning("Search methods implemented: {}".format(
                    DEFAULT.searchMethodChoices))

    @dupMethod.setter
    def dupMethod(self, value):
        """
        Checks if the duplicate method is implemented
        Warns the user if not and fall back to default
        """
        if value in DEFAULT.dupMethodChoices:
            self._dupMethod = value
        else:
            self._dupMethod = DEFAULT.duplicateMethod
            self.logger.warning(
                    "'{}' is not a duplicate method implemented".format(value))
            self.logger.warning(
                    "Falling back to default: {}".format(DEFAULT.dupMethod))
            self.logger.warning("Duplicate methods implemented: {}".format(
                    DEFAULT.dupMethodChoices))

    def build_graph(self):
        """
        Test all the possible links between the list of sidecars and the
        description dictionnaries and build a graph from it
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
            data (dict): Dictionnary data of a sidecar
            criteria (dict): Dictionnary criteria

        Returns:
            boolean
        """
        def compare(name, pattern):
            if self.searchMethod == "re":
                return bool(re.search(pattern, str(name)))

            else:
                return fnmatch(str(name), str(pattern))


        result = []
        for tag, pattern in iteritems(criteria):
            name = data.get(tag)

            if isinstance(name, list):
                try:
                    subResult = [
                            len(name)==len(pattern),
                            isinstance(pattern, list),
                            ]
                    for subName, subPattern in zip(name, pattern):
                        subResult.append(compare(subName, subPattern))
                except:
                    subResult = [False]

                result.append(all(subResult))

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
        acquisitions = []
        self.logger.info("Sidecars pairing:")
        for sidecar, descriptions in iteritems(self.graph):
            sidecarName = os.path.basename(sidecar.root)

            #only one description for the sidecar
            if len(descriptions) == 1:
                desc = descriptions[0]

                if self._dcmTagLabel:
                    desc = self.addDcmTagLabel(sidecar, desc)

                acq = Acquisition(participant, srcSidecar=sidecar,
                                    **desc)

                if acq.intendedFor == [None]:
                    acqIndex = self.getAcqIndex(desc)
                    dst = acq.dstRoot.split(os.path.sep)[1:]
                    dst = os.path.sep.join(dst)
                    self.dstImage[acqIndex].append(dst)

                acquisitions.append(acq)

                self.logger.info("{}  <-  {}".format(acq.suffix, sidecarName))

            #sidecar with no link
            elif len(descriptions) == 0:
                self.logger.info("No Pairing  <-  {}".format(sidecarName))

            #sidecar with several links
            else:
                self.logger.warning(
                        "Several Pairing  <-  {}".format(sidecarName))
                for desc in descriptions:
                    acq = Acquisition(participant, **desc)
                    self.logger.warning("    ->  " + acq.suffix)

        #fmap dataType at the end of acquisitions
        for idx, acq in enumerate(acquisitions):
            if acq.dataType == "fmap":
                 acquisitions.append(acquisitions.pop(idx))

        self.acquisitions = acquisitions
        return acquisitions

    def addDcmTagLabel(self, sidecar, desc):
        """
        Add TaskLabel to customLabels
        """
        descWithTask = desc.copy()
        if self.dcmTagLabel["dcmTag"] in sidecar.data.keys():
            dcmTag = sidecar.data.get(self.dcmTagLabel["dcmTag"])
            patterns = self.dcmTagLabel["expression"]

            if isinstance(patterns, list):
                tmpDcmTagLabel = []
                for pattern in patterns :
                    dcmTagLabel = re.search(pattern, dcmTag)
                    if dcmTagLabel:
                        dcmTagLabel = '_'.join(map(str, dcmTagLabel.groups()))
                        tmpDcmTagLabel.append(dcmTagLabel)

                dcmTagLabel = '_'.join(tmpDcmTagLabel)
            else:
                dcmTagLabel = re.search(pattern, dcmTag)
                if dcmTagLabel:
                    dcmTagLabel = '_'.join(map(str, dcmTagLabel.groups()))


            if "customLabels" in desc.keys():
                descWithTask["customLabels"] = dcmTagLabel + '_' + descWithTask["customLabels"]
            else:
                descWithTask["customLabels"] = dcmTagLabel

        return descWithTask

    def find_runs(self):
        """
        Check if there is duplicate destination roots in the acquisitions
        and add '_run-' to the customLabels of the acquisition
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

            for key, locs in iteritems(tally):
                if len(locs) > 1:
                    yield key, locs

        dstRoots = [_.dstRoot for _ in self.acquisitions]

        templateDup = DEFAULT.runTpl
        if self.dupMethod == 'dup':
            templateDup = DEFAULT.dupTpl

        for dstRoot, dup in duplicates(dstRoots):
            self.logger.info("{} has {} runs".format(dstRoot, len(dup)))
            self.logger.info("Adding {} information to the acquisition".format(self.dupMethod))

            if self.dupMethod == 'dup':
                dup = dup[0:-1]
                for runNum, acqInd in enumerate(dup):
                    runStr = templateDup.format(runNum+1)
                    self.acquisitions[acqInd].modalityLabel += runStr
            else:
                for runNum, acqInd in enumerate(dup):
                    runStr = templateDup.format(runNum+1)
                    self.acquisitions[acqInd].customLabels += runStr

    def getAcqIndex(self, description):
        for idx, desc in enumerate(self.descriptions):
            if isDictsEqual(desc, description):
                return idx
