# -*- coding: utf-8 -*-

"""k"""


from os.path import join as opj
from future.utils import iteritems
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
            return '_'.join([self.name,self.session])
        else:
            return self.name

    def hasSession(self):
        """ Check if a session is set

        Returns:
            Boolean
        """
        return self.session.strip() != DEFAULT.session


class Acquisition(object):
    """ Class representing an acquisition

    Args:
        participant (Participant): A participant object
        dataType (str): A functional group of MRI data (ex: func, anat ...)
        modalityLabel (str): The modality of the acquisition
                (ex: T1w, T2w, bold ...)
        customLabels: Optional labels, either string or dict format (ex: "task-rest" or {"task"':"rest"})
        srcSidecar (Sidecar): Optional sidecar object
    """

    def __init__(
        self,
        participant,
        dataType,
        modalityLabel,
        customLabels,
        srcSidecar=None,
        sidecarChanges=None,
        intendedFor=None,
        IntendedFor=None,
        **kwargs
    ):

        self._intendedFor = None

        self.participant = participant
        self.dataType = dataType
        self.modalityLabel = modalityLabel
        print(customLabels)
        self._customLabels = self.verifyBIDSconformity(customLabels)
        self.srcSidecar = srcSidecar
        if sidecarChanges is None:
            self.sidecarChanges = {}
        else:
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
    def customLabelsString(self):
        return self.customLabels2string()

    def customLabels2string(self):
        """
        Returns:
            A string '<customLabels>'
        """
        # sort labels alphabetically 
        sortedLabels = sorted(self._customLabels.keys(), key=lambda x:x.lower())
        # create list of <entity>-<label> strings
        labels = ['-'.join([ent, self._customLabels[ent]]) for ent in sortedLabels]
        #join the string with underscores
        return '_'.join(labels)

    def verifyBIDSconformity(self, labels):
        """
        Returns:
            A dictionary for custom labels
        """

        labelDict = {}
        if type(labels) == str:
            if len(labels.split("_")) == 1:
                #if only one entry and not bids conform, put 'acq' entity 
                labelDict = {'acq':labels}
            else:
                labelDict = dict(x.split("-") for x in labels.split("_"))
        else:
            labelDict = labels

        # TODO -> check for entities available in this BIDS version ? 
        customEntities = ["task","acq","ce","trc","rec","dir","echo","flip","inv","mt","part","recording","proc","space"]

        for k,v in labelDict.items():
            if k not in customEntities or '_' in v or '-' in v or v == '':
                #raise warning if label not conform to BIDS specification
                print("Warning! Output file name might not be BIDS conform..")

        return labelDict

    @property
    def suffix(self):
        """ The suffix to build filenames

        Returns:
            A string '_<modalityLabel>' or '_<customLabels>_<modalityLabel>'
        """
        if self.customLabelsString.strip() == "":
            return '_'.join(['',self.modalityLabel])
        else:
            return '_'.join(['',self.customLabelsString, self.modalityLabel])

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
            self.participant.prefix + self.suffix,
        )

    @property
    def intendedFor(self):
        return self._intendedFor

    @intendedFor.setter
    def intendedFor(self, value):
        if isinstance(value, list):
            self._intendedFor = value
        else:
            self._intendedFor = [value]

    def dstSidecarData(self, descriptions):
        """
        """
        data = self.srcSidecar.origData
        data["Dcm2bidsVersion"] = __version__

        # intendedFor key
        if self.intendedFor != [None]:
            intendedValue = []
            for index in self.intendedFor:
                intendedDesc = descriptions[index]

                session = self.participant.session
                dataType = intendedDesc["dataType"]

                niiFile = self.participant.prefix
                if intendedDesc.get("customLabelsString", "") != "":
                    niiFile += '_' + intendedDesc.get("customLabelsString", "")
                niiFile += '_' + intendedDesc["modalityLabel"]
                niiFile += ".nii.gz"

                intendedValue.append(opj(session, dataType, niiFile).replace("\\", "/"))

            if len(intendedValue) == 1:
                data["IntendedFor"] = intendedValue[0]
            else:
                data["IntendedFor"] = intendedValue

        # sidecarChanges
        for key, value in iteritems(self.sidecarChanges):
            data[key] = value

        return data
