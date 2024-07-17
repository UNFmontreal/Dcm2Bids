#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure
"""

import argparse
import logging
import platform
import sys
import os
from pathlib import Path
from datetime import datetime
from dcm2bids.dcm2bids_gen import Dcm2BidsGen
from dcm2bids.utils.utils import DEFAULT
from dcm2bids.utils.tools import dcm2niix_version, check_latest
from dcm2bids.participant import Participant
from dcm2bids.utils.logger import setup_logging
from dcm2bids.version import __version__


def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__, epilog=DEFAULT.doc,
                                formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument("-d", "--dicom_dir",
                   required=True, nargs="+",
                   help="DICOM directory(ies) or archive(s) (" +
                        DEFAULT.arch_extensions + ").")

    p.add_argument("-p", "--participant",
                   required=True,
                   help="Participant ID.")

    p.add_argument("-s", "--session",
                   required=False,
                   default=DEFAULT.cli_session,
                   help="Session ID. [%(default)s]")

    p.add_argument("-c", "--config",
                   required=True,
                   help="JSON configuration file (see example/config.json).")

    p.add_argument("-o", "--output_dir",
                   required=False,
                   default=DEFAULT.output_dir,
                   help="Output BIDS directory. [%(default)s]")

    g = p.add_mutually_exclusive_group()
    g.add_argument("--auto_extract_entities",
                   action='store_true',
                   help="If set, it will automatically try to extract entity"
                   "information [task, dir, echo] based on the suffix and datatype."
                   " [%(default)s]")

    g.add_argument("--do_not_reorder_entities",
                   action='store_true',
                   help="If set, it will not reorder entities according to the relative "
                        "ordering indicated in the BIDS specification and use the "
                        "order defined in custom_entities by the user.\n"
                        "Cannot be used with --auto_extract_entities. "
                        " [%(default)s]")

    p.add_argument("--bids_validate",
                   action='store_true',
                   help="If set, once your conversion is done it "
                        "will check if your output folder is BIDS valid. [%(default)s]"
                        "\nbids-validator needs to be installed check: "
                        f"{DEFAULT.link_bids_validator}")

    p.add_argument("--force_dcm2bids",
                   action="store_true",
                   help="Overwrite previous temporary dcm2bids "
                        "output if it exists.")

    p.add_argument("--skip_dcm2niix",
                   action="store_true",
                   help="Skip dcm2niix conversion. "
                        "Option -d should contains NIFTI and json files.")

    p.add_argument("--clobber",
                   action="store_true",
                   help="Overwrite output if it exists.")

    p.add_argument("-l", "--log_level",
                   required=False,
                   default=DEFAULT.cli_log_level,
                   choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                   help="Set logging level to the console. [%(default)s]")

    p.add_argument("-v", "--version",
                   action="version",
                   version=f"dcm2bids version:\t{__version__}\n"
                   f"Based on BIDS version:\t{DEFAULT.bids_version}",
                   help="Report dcm2bids version and the BIDS version.")

    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    participant = Participant(args.participant, args.session)
    log_dir = Path(args.output_dir) / DEFAULT.tmp_dir_name / "log"
    log_file = (log_dir /
                f"{participant.prefix}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log")
    log_dir.mkdir(parents=True, exist_ok=True)

    setup_logging(args.log_level, log_file)

    logger = logging.getLogger(__name__)

    logger.info("--- dcm2bids start ---")
    logger.info("Running the following command: " + " ".join(sys.argv))
    logger.info("OS version: %s", platform.platform())
    logger.info("Python version: %s", sys.version.replace("\n", ""))
    logger.info(f"dcm2bids version: { __version__}")
    logger.info(f"dcm2niix version: {dcm2niix_version()}")
    logger.info("Checking for software update")

    check_latest("dcm2bids")
    check_latest("dcm2niix")

    logger.info(f"participant: {participant.name}")
    if participant.session:
        logger.info(f"session: {participant.session}")
    logger.info(f"config: {os.path.realpath(args.config)}")
    logger.info(f"BIDS directory: {os.path.realpath(args.output_dir)}")
    logger.info(f"Auto extract entities: {args.auto_extract_entities}")
    logger.info(f"Reorder entities: {not args.do_not_reorder_entities}")
    logger.info(f"Validate BIDS: {args.bids_validate}\n")

    app = Dcm2BidsGen(**vars(args)).run()

    logger.info(f"Logs saved in {log_file}")
    logger.info("--- dcm2bids end ---")

    return app


if __name__ == "__main__":
    main()
