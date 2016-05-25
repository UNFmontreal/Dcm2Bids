# -*- coding: utf-8 -*-
import math

__author__ = "Mathieu Desrosiers"
__copyright__ = "Copyright (C) 2014, TOAD"
__credits__ = ["Mathieu Desrosiers"]

class Ascconv(object):

    def __init__(self, filename):
        self.__fileName = filename
        self.__ascconvFound = False
        self.__phaseEncodingDirection = 1
        self.__patFactor = 1
        self.__epiFactor = 1
        self.__phaseResolution = 1
        self.__phaseOversampling = 1
        self.__numberArrayCoil = 0
        self.__initialize()

    def __repr__(self):
        return "filename={}, phaseEncodingDirection={}, patFactor={}, epiFactor={}, phaseResolution={}, phaseOversampling ={}" \
                    .format(self.__fileName,
                            self.__phaseEncodingDirection,
                            self.__patFactor,
                            self.__epiFactor,
                            self.__phaseResolution,
                            self.__phaseOversampling)

    def isValid(self):
        return self.__ascconvFound

    def getFileName(self):
        return self.__fileName

    def getPhaseEncodingDirection(self):
        return self.__phaseEncodingDirection

    def getPatFactor(self):
        return self.__patFactor

    def getEpiFactor(self):
        return self.__epiFactor

    def getPhaseResolution(self):
        return self.__phaseResolution

    def getPhaseOversampling(self):
        return  self.__phaseOversampling

    def getNumberArrayCoil(self):
        return self.__numberArrayCoil


    def __initialize(self):
        with open(self.__fileName, 'r') as f:
            ascconv = []
            for line in f.readlines():
                if "### ASCCONV BEGIN ###" in line:
                    self.__ascconvFound = True
                if "### ASCCONV END ###" in line:
                    break
                if self.__ascconvFound:
                    ascconv.append(line)

            for line in ascconv:
                line = line.lower()

                if "coil" in line and "meas" in line and "lrxchannelconnected" in line:
                    self.__numberArrayCoil += 1

                elif "sslicearray.asslice" in line and ".dinplanerot" in line:
                    self.__phaseEncodingDirection = int(self.__returnPhaseEncodingDirection(line))

                elif "spat.laccelfactpe" in line:
                    try:
                        self.__patFactor = float(line.split("=")[-1].strip())
                    except ValueError:
                        pass
                elif "skspace.lphaseencodinglines" in line:
                    try:
                        self.__epiFactor = int(line.split("=")[-1].strip())
                    except ValueError:
                        pass
                elif "skspace.dphaseresolution" in line:
                    try:
                        self.__phaseResolution= int(line.split("=")[-1].strip())
                    except ValueError:
                        pass

                elif "skspace.dphaseoversamplingfordialog" in line:
                    try:
                        self.__phaseOversampling = int(line.split("=")[-1].strip())
                    except ValueError:
                        pass

    def __returnPhaseEncodingDirection(self, line):

        tolerance = 0.2
        try:
            value = float(line.split("=")[-1].strip())
        except ValueError:
            return 1

        if value < tolerance and value > -tolerance:
           return 1  #between -0.2 and 0.2  A>>P

        if (value > math.pi - tolerance) or (value < tolerance - math.pi):
            return 0  #greater than  2.94  or smaller than -2.94  #P>>A

        if (value > (math.pi/2) - tolerance) and (value < (math.pi/2)+tolerance):
            return 2  #R>>L

        if (value < math.copysign((math.pi/2)-tolerance,-0.0)) and (value > math.copysign((math.pi/2)+tolerance, -0.0)):
             return 3  #L>>R

        return 1
