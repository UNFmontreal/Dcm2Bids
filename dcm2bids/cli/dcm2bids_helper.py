# -*- coding: utf-8 -*-

"""
Converts DICOM files to NIfTI files including their JSON sidecars in a
temporary directory which can be inspected to make a dc2mbids config file.
"""
import argparse
import logging
import platform
import sys
import os
from pathlib import Path
from datetime import datetime
from dcm2bids.dcm2niix_gen import Dcm2niixGen
from dcm2bids.utils.utils import DEFAULT
from dcm2bids.utils.tools import dcm2niix_version, check_latest
from dcm2bids.utils.logger import setup_logging
from dcm2bids.version import __version__


def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__, epilog=DEFAULT.doc,
                                formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument("-d", "--dicom_dir",
                   required=True, nargs="+",
                   help="DICOM directory(ies) or archive(s) (" +
                        DEFAULT.arch_extensions + ").")

    p.add_argument("-o", "--output_dir",
                   required=False,
                   default=Path(DEFAULT.output_dir) / DEFAULT.tmp_dir_name /
                   DEFAULT.helper_dir,
                   help="Output directory. (Default: [%(default)s]")

    p.add_argument("-n", "--nest",
                   nargs="?", const=True, default=False, required=False,
                   help="Nest a directory in <output_dir>. Useful if many helper "
                        "runs are needed\nto make a config file due to slight "
                        "variations in MRI acquisitions.\n"
                        "Defaults to DICOM_DIR if no name is provided.\n"
                        "(Default: [%(default)s])")

    p.add_argument('--force', '--force_dcm2bids',
                   dest='overwrite', action='store_true',
                   help='Force command to overwrite existing output files.')

    p.add_argument("-l", "--log_level",
                   required=False,
                   default=DEFAULT.cli_log_level,
                   choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                   help="Set logging level to the console. [%(default)s]")

    return p


def main():
    """Let's go"""
    parser = _build_arg_parser()
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    if args.output_dir != parser.get_default('output_dir'):
        out_dir = (Path(args.output_dir)
                   / DEFAULT.tmp_dir_name
                   / DEFAULT.helper_dir)

        log_file = (Path(args.output_dir)
                    / DEFAULT.tmp_dir_name
                    / "log"
                    / f"helper_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log")
    else:
        log_file = (Path(DEFAULT.output_dir)
                    / DEFAULT.tmp_dir_name
                    / "log"
                    / f"helper_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log")
    if args.nest:
        if isinstance(args.nest, str):
            log_file = Path(
              str(log_file).replace("helper_",
                                    f"helper_{args.nest.replace(os.path.sep, '-')}_"))
            out_dir = out_dir / args.nest
        else:
            log_file = Path(str(log_file).replace(
              "helper_", f"helper_{args.dicom_dir[0].replace(os.path.sep, '-')}_")
                            )
            out_dir = out_dir / args.dicom_dir[0]

    log_file.parent.mkdir(parents=True, exist_ok=True)

    setup_logging(args.log_level, log_file)

    logger = logging.getLogger(__name__)

    logger.info("--- dcm2bids_helper start ---")
    logger.info("Running the following command: " + " ".join(sys.argv))
    logger.info("OS version: %s", platform.platform())
    logger.info("Python version: %s", sys.version.replace("\n", ""))
    logger.info(f"dcm2bids version: { __version__}")
    logger.info(f"dcm2niix version: {dcm2niix_version()}")
    logger.info("Checking for software update")

    check_latest("dcm2bids")
    check_latest("dcm2niix")

    app = Dcm2niixGen(dicom_dirs=args.dicom_dir, bids_dir=out_dir, helper=True)

    rsl = app.run(force=args.overwrite)

    logger.info(f"Helper files in: {out_dir}\n")
    logger.info(f"Log file saved at {log_file}")
    logger.info("--- dcm2bids_helper end ---")

    return rsl


if __name__ == "__main__":
    main()
