# -*- coding: utf-8 -*-


import os


class DEFAULT(object):
    """ Default values of the package"""

    doc = "Documentation at https://github.com/unfmontreal/Dcm2Bids"

    # cli dcm2bids
    cliSession = ""
    cliOutputDir = os.getcwd()
    cliLogLevel = "INFO"

    # dcm2bids.py
    outputDir = cliOutputDir
    session = cliSession  # also Participant object
    clobber = False
    forceDcm2niix = False
    defaceTpl = None
    logLevel = "WARNING"

    # dcm2niix.py
    dcm2niixOptions = "-b y -ba y -z y -f '%3s_%f_%p_%t'"
    dcm2niixVersion = "v1.0.20181125"

    # sidecar.py
    compKeys = ["SeriesNumber", "AcquisitionTime", "SidecarFilename"]
    searchMethod = "fnmatch"
    searchMethodChoices = ["fnmatch", "re"]
    runTpl = "_run-{:02d}"
    caseSensitive = True

    # Entity table:
    # https://bids-specification.readthedocs.io/en/v1.7.0/99-appendices/04-entity-table.html
    entityTableKeys = ["sub", "ses", "task", "acq", "ce", "rec", "dir",
                       "run", "mod", "echo", "flip", "inv", "mt", "part",
                       "recording"]

    # misc
    tmpDirName = "tmp_dcm2bids"
    helperDir = "helper"


def splitext_(path, extensions=None):
    """ Split the extension from a pathname
    Handle case with extensions with '.' in it

    Args:
        path (str): A path to split
        extensions (list): List of special extensions

    Returns:
        (root, ext): ext may be empty
    """
    if extensions is None:
        extensions = [".nii.gz"]

    for ext in extensions:
        if path.endswith(ext):
            return path[: -len(ext)], path[-len(ext) :]
    return os.path.splitext(path)
