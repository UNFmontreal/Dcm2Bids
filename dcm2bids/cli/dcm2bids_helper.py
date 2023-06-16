# -*- coding: utf-8 -*-

"""
Converts DICOM files to NIfTI files including their JSON sidecars in a
temporary directory which can be inspected to make a dc2mbids config file.
"""
import logging
import argparse
import sys
import os
from os.path import join as opj
from pathlib import Path
from datetime import datetime
from dcm2bids.dcm2niix_gen import Dcm2niixGen
from dcm2bids.utils.args import add_overwrite_arg, assert_dirs_empty
from dcm2bids.utils.utils import DEFAULT
from dcm2bids.utils.logger import setup_logging

def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__, epilog=DEFAULT.doc,
                                formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument("-d", "--dicom_dir",
                   required=True, nargs="+",
                   help="DICOM files directory.")

    p.add_argument("-o", "--output_dir",
                   required=False,
                   default=Path(DEFAULT.cliOutputDir) / DEFAULT.tmpDirName / DEFAULT.helperDir,
                   help=f'Output directory. (Default: [%(default)s]')

    p.add_argument("-n", "--nest",
                   nargs="?", const=True, default=False, required=False,
                   help=f"Nest a directory in <output_dir>. Useful if many helper runs are needed\n"
                        f"to make a config file due to slight variations in MRI acquisitions.\n"
                        f"Defaults to DICOM_DIR if no name is provided.\n"
                        f"(Default: [%(default)s])")

    p.add_argument('--force', '--force_dcm2niix',
                   dest='overwrite', action='store_true',
                   help='Force command to overwrite existing output files.')

    return p

def main():
    """Let's go"""
    parser = _build_arg_parser()
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    log_path = Path(DEFAULT.cliOutputDir) / DEFAULT.tmpDirName / "log" / f"helper_{datetime.now().isoformat().replace(':', '')}.log"
    if args.nest:
        if isinstance(args.nest, str):
            log_path = Path(str(log_path).replace("helper_", f"helper_{args.nest.replace(os.path.sep, '-')}_"))
            out_dir = out_dir / args.nest
        else:
            log_path = Path(str(log_path).replace("helper_", f"helper_{args.dicom_dir[0].replace(os.path.sep, '-')}_"))
            out_dir = out_dir / args.dicom_dir[0]

    log_path.parent.mkdir(parents=True, exist_ok=True)
    setup_logging("info", log_path)
    logger = logging.getLogger(__name__)

    logger.info("Running the following command: \n" + " ".join(sys.argv) + "\n")

    assert_dirs_empty(parser, args, out_dir)

    app = Dcm2niixGen(dicomDirs = args.dicom_dir, bidsDir = out_dir, helper = True)

    rsl = app.run(force=args.overwrite)
    logger.info(f"Helper files in: {out_dir}\n")
    logger.info(f"Log file saved at {log_path}")

    return rsl

if __name__ == "__main__":
    main()
