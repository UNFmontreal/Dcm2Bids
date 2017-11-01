# -*- coding: utf-8 -*-


import itertools
import fnmatch
import logging
import os
from collections import defaultdict, OrderedDict
from future.utils import iteritems
from .structure import Acquisition
from .utils import load_json, splitext_


class Sidecarparser(object):

    def __init__(self, sidecars, descriptions):
        self.sidecars = sidecars
        self.descriptions = descriptions
        self.logger = logging.getLogger("dcm2bids")
        self.graph = self._generateGraph()
        self.acquisitions = self._generateAcquisitions()
        self.findRuns()


    def _generateGraph(self):
        graph = OrderedDict((_, []) for _ in self.sidecars)
        for sidecar, index in itertools.product(
                self.sidecars, range(len(self.descriptions))):
            self._sidecar = load_json(sidecar)
            self._sidecar["SidecarFilename"] = os.path.basename(sidecar)
            criteria = self.descriptions[index]["criteria"]
            if criteria and self._respect(criteria):
                graph[sidecar].append(index)
        return graph


    def _generateAcquisitions(self):
        rsl = []
        print("")
        print("Sidecars matching:")
        for sidecar, match_descs in iteritems(self.graph):
            base = splitext_(sidecar)[0]
            basename = os.path.basename(sidecar)

            if len(basename) > 62:
                basename = basename[:30] + ".." + basename[-30:]

            if len(match_descs) == 1:
                print("MATCH           {}".format(basename))
                acq = self._acquisition(
                        base, self.descriptions[match_descs[0]])
                rsl.append(acq)

            elif len(match_descs) == 0:
                print("NO MATCH        {}".format(basename))

            else:
                print("SEVERAL MATCHES {}".format(basename))
        return rsl


    def findRuns(self):
        def list_duplicates(seq):
            """
            http://stackoverflow.com/a/5419576
            """
            tally = defaultdict(list)
            for i, item in enumerate(seq):
                tally[item].append(i)
            return ((key,locs) for key,locs in tally.items() if len(locs)>1)

        print("")
        print("Checking if a description matches several sidecars ...")
        suffixes = [_.suffix for _ in self.acquisitions]
        for suffix, dup in sorted(list_duplicates(suffixes)):
            print("'{}' has several runs".format(suffix))
            for run, acq_index in enumerate(dup):
                runStr = "run-{:02d}".format(run+1)
                acq = self.acquisitions[acq_index]
                if acq.customLabels is None:
                    acq.customLabels = runStr
                else:
                    acq.customLabels += "_" + runStr
        print("")


    def _acquisition(self, base, desc):
        acq = Acquisition(base, desc["dataType"], desc["modalityLabel"])
        if "customLabels" in desc:
            acq.customLabels = desc["customLabels"]
        else:
            acq.customLabels = None
        return acq


    def _respect(self, criteria):
        rsl = []
        for tag, pattern in iteritems(criteria):
            name = self._sidecar.get(tag)
            pat = str(pattern)
            if isinstance(name, list):
                subRsl = []
                for subName in name:
                    subRsl.append(fnmatch.fnmatch(str(subName), pat))
                rsl.append(any(subRsl))
            else:
                rsl.append(fnmatch.fnmatch(str(name), pat))
        return all(rsl)

