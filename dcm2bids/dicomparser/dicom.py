import os
import sys
import struct

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from pydicom.filereader import read_file
from pydicom.tag import Tag
from pydicom.errors import InvalidDicomError

from ascconv import Ascconv
from lib import util


manufacturers = ['Philips', 'GE', 'SIEMENS']

class Dicom(Ascconv):

    def __init__(self, filename):
        self.__filename = filename
        self.__isDicom = False
        self.__manufacturer = None
        self.__patientName = None
        self.__seriesDescription = None
        self.__seriesNumber = None
        self.__instanceNumber = None
        self.__channel = None
        self.__bandwidthPerPixelPhaseEncode = None
        self.__echoTime = None
        self.__echoSpacing = None
        self.__initialized()

    def __repr__(self):
        return "filename = {}, manufacturer ={}, patientName={}, seriesDescription={}, seriesNumber={}, instanceNumber={}, echoTime={}, channel={}, isDicom = {}"\
                .format(self.__filename, self.__manufacturer, self.__patientName, self.__seriesDescription, self.__seriesNumber, self.__instanceNumber, self.__echoTime, self.__channel, self.__isDicom)

    def __initialized(self):

        try:
            header =  read_file(self.__filename, defer_size=None, stop_before_pixels=True)

        except InvalidDicomError:
            self.__isDicom = False
            return
        try:

            #find the manufacturer
            self.__manufacturer = 'UNKNOWN'
            if 'Manufacturer' in header:
                for manufacturer in manufacturers:
                    if manufacturer in header.Manufacturer:
                        self.__manufacturer = manufacturer

            self.__patientName = util.slugify(header.PatientName)
            self.__seriesDescription = util.slugify(header.SeriesDescription)
            self.__seriesNumber = header.SeriesNumber
            self.__instanceNumber = header.InstanceNumber
            self.__echoTime = header.EchoTime
            self.__isDicom = True

        except AttributeError as a:
            if "EchoTime" in a.message:
                try:
                    self.__echoTime = header[Tag((0x2001, 0x1025))].value
                    self.__isDicom = True
                except KeyError as k:
                    self.__isDicom = False
            else:
                 self.__isDicom = False

        if self.isSiemens():
            #inherith Siemens ascconv properties
            Ascconv.__init__(self, self.__filename)
            bandwidthPerPixelPhaseEncodeTag = Tag((0x0019, 0x1028))

            try:
                if header.has_key(bandwidthPerPixelPhaseEncodeTag):
                    val = header[bandwidthPerPixelPhaseEncodeTag].value
                    try:
                        self.__bandwidthPerPixelPhaseEncode = float(val)
                    except ValueError:
                        # some data have wrong VR in dicom, try to unpack
                        self.__bandwidthPerPixelPhaseEncode = struct.unpack('d', val)[0]

                self.__echoSpacing = 1/(self.__bandwidthPerPixelPhaseEncode* self.getEpiFactor()) *1000.0 * \
                              self.getPatFactor() * self.getPhaseResolution() * \
                              self.getPhaseOversampling()

            except (KeyError, IndexError, TypeError, ValueError):
                self.__echoSpacing = None


    def getFileName(self):
        return self.__filename

    def getSequenceName(self):
        return "{:02d}-{}".format(int(self.__seriesNumber), self.__seriesDescription)

    def getSessionName(self):
        return self.__patientName

    def getSeriesDescription(self):
        return self.__seriesDescription

    def getSeriesNumber(self):
        return self.__seriesNumber

    def getInstanceNumber(self):
        return self.__instanceNumber

    def getEchoTime(self):
        return self.__echoTime

    def getEchoSpacing(self):
        return self.__echoSpacing

    def isDicom(self):
        return self.__isDicom

    def isSiemens(self):
        return self.__manufacturer == 'SIEMENS'
