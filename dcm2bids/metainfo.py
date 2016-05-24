# -*- coding: utf-8 -*-

JSON = {
    "RepetitionTime": "",
    "TaskName": "",
    "Manufacturer": (0x0008, 0x0070),
    "ManufacturersModelName": (0x0008, 0x1090),
    "MagneticFieldStrength": (0x0018, 0x0087),
    "HardcopyDeviceSoftwareVersion": (0x0018, 0x101A),
    "ReceiveCoilName": "n/a",
    "GradientSetType": "n/a",
    "MRTransmitCoilSequence": (0x0018, 0x9049),
    "MatrixCoilMode": "n/a",
    "CoilCombinationMethod": "n/a",
    "PulseSequenceType": "n/a",
    "PulseSequenceDetails": "n/a",
    "NumberShots": "n/a",
    "ParallelReductionFactorInPlane": (0x0018, 0x9069),
    "ParallelAcquisitionTechnique": (0x0018, 0x9078),
    "PartialFourier": (0x0018, 0x9081),
    "PartialFourierDirection": (0x0018, 0x9036),
    "PhaseEncodingDirection": "n/a",
    "EffectiveEchoSpacing": "n/a",
    "EchoTime": (0x0018, 0x0081),
    "SliceTiming": "n/a",
    "SliceEncodingDirection": "n/a",
    "FlipAngle": (0x0018, 0x1314),
    "MultibandAccelerationFactor": "n/a",
    "Instructions": "n/a",
    "TaskDescription": "n/a",
    "CogAtlasID": "n/a",
    "CogPOID": "n/a"
    }


class Metainfo(object):
    """
    """

    def __init__(self, ds):
        self.masterJson = JSON
        self.ds = ds
        self.passed = {}
        self.failed = {}
        self.__setJsons()


    def __dsHasTag(self, tag):
        try:
            self.ds[tag]
            return True
        except:
            return False


    def __setJsons(self):
        for key, tag in self.masterJson.iteritems():
            if self.__dsHasTag(tag):
                self.passed[key] = self.ds[tag].value
            else:
                self.failed[key] = "n/a"


    def writeJsons(self, outputWithoutExt)
        passedFile = "{}.json".format(outputWithoutExt)
            utils.writingJSON(passed, passedJsonFile)
            failedJsonFile = "{}_failed.json".format(acquisition.getOutputWithoutExt())
            utils.writingJSON(failed, failedJsonFile)
