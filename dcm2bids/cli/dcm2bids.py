#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure
"""

import argparse

from dcm2bids.dcm2bids_gen import Dcm2BidsGen
from dcm2bids.utils.tools import check_latest
from dcm2bids.utils.utils import DEFAULT
from dcm2bids.version import __version__

def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__, epilog=DEFAULT.doc,
                                formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument("-d", "--dicom_dir",
                   required=True, nargs="+",
                   help="DICOM directory(ies).")

    p.add_argument("-p", "--participant",
                   required=True,
                   help="Participant ID.")

    p.add_argument("-s", "--session",
                   required=False,
                   default=DEFAULT.cliSession,
                   help="Session ID. [%(default)s]")

    p.add_argument("-c", "--config",
                   required=True,
                   help="JSON configuration file (see example/config.json).")

    p.add_argument("-o", "--output_dir",
                   required=False,
                   default=DEFAULT.cliOutputDir,
                   help="Output BIDS directory. [%(default)s]")

    p.add_argument("--forceDcm2niix",
                   action="store_true",
                   help="Overwrite previous temporary dcm2niix "
                        "output if it exists.")

    p.add_argument("--clobber",
                   action="store_true",
                   help="Overwrite output if it exists.")

    p.add_argument("-l", "--log_level",
                   required=False,
                   default=DEFAULT.cliLogLevel,
                   choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                   help="Set logging level. [%(default)s]")

    p.add_argument("-v", "--version",
                   action="version",
                   version=f"dcm2bids version:\t{__version__}\nBased on BIDS version:\t{DEFAULT.bids_version}",
                   help="Report dcm2bids version and the BIDS version.")

    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    check_latest()
    check_latest("dcm2niix")

    app = Dcm2BidsGen(**vars(args))
    return app.run()


if __name__ == "__main__":
    main()
