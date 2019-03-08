# -*- coding: utf-8 -*-


import itertools
import logging
import os
import re
from collections import defaultdict, OrderedDict
from fnmatch import fnmatch
from future.utils import iteritems
from .structure import Acquisition
from .utils import DEFAULT, load_json, splitext_


class Sidecar(object):
    """ A sidecar object

    Args:
        filename (str): Path of a JSON sidecar
        keyComp (str): A key from the JSON sidecar to compare sidecars
                     default="SeriesNumber"
    """

    def __init__(self, filename, keyComp=DEFAULT.keyComp):
        self._origData = {}
        self._data = {}

        self.filename = filename
        self.root, _ = splitext_(filename)
        self.data = filename
        self.keyComp = keyComp


    def __lt__(self, other):
        selfComp = self._data[self.keyComp]
        otherComp = other.data[self.keyComp]
        if selfComp == otherComp:
            return self.root < other.root
        else:
            return selfComp < otherComp


    def __eq__(self, other):
        return self._data == other.data


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
            searchMethod=DEFAULT.searchMethod):
        self.logger = logging.getLogger(__name__)

        self._searchMethod = ""
        self.graph = OrderedDict()
        self.aquisitions = []

        self.sidecars = sidecars
        self.descriptions = descriptions
        self.searchMethod = searchMethod


    @property
    def searchMethod(self):
        return self._searchMethod


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
                subResult = []
                for subName in name:
                    subResult.append(compare(subName, pattern))
                result.append(any(subResult))

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
                acq = Acquisition(participant, srcSidecar=sidecar, **desc)
                acquisitions.append(acq)

                self.logger.info("{} <- {}".format(
                    acq.dstRoot, sidecarName))

            #sidecar with no link
            elif len(descriptions) == 0:
                self.logger.info("No Pairing <- {}".format(sidecarName))

            #sidecar with several links
            else:
                self.logger.info("Several Pairing <- {}".format(sidecarName))
                for desc in descriptions:
                    acq = Acquisition(participant, **desc)
                    self.logger.info(acq.dstRoot())

        self.acquisitions = acquisitions
        return acquisitions


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


        self.logger.info(
                "Checking if a description is paired with several sidecars")

        dstRoots = [_.dstRoot for _ in self.acquisitions]
        for dstRoot, dup in duplicates(dstRoots):
            self.logger.info("{} has {} runs".format(dstRoot, len(dup)))

            for runNum, acqInd in enumerate(dup):
                runStr = DEFAULT.runTpl.format(runNum+1)
                self.acquisitions[acqInd].customLabels += runStr

