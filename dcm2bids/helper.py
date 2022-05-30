# -*- coding: utf-8 -*-

"""helper module"""

import argparse
import os
from pathlib import Path
import sys

from dcm2bids.dcm2niix import Dcm2niix
from dcm2bids.utils import DEFAULT, assert_dirs_empty


def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__, epilog=DEFAULT.EPILOG,
                                formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument("-d", "--dicom_dir",
                   type=Path,
                   required=True, nargs="+",
                   help="DICOM files directory.")

    p.add_argument("-o", "--output_dir",
                   required=False, default=Path.cwd(),
                   type=Path,
                   help="Output BIDS directory. "
                        "(Default: %(default)s)")

    p.add_argument('--force',
                   dest='overwrite', action='store_true',
                   help='Force command to overwrite existing output files.')

    return p


def main():
    """Let's go"""
    parser = _build_arg_parser()
    args = parser.parse_args()
    out_folder = args.output_dir / DEFAULT.tmpDirName / DEFAULT.helperDir
    assert_dirs_empty(parser, args, out_folder)
    app = Dcm2niix(dicomDirs=args.dicom_dir, bidsDir=args.output_dir)
    rsl = app.run()
    print(f"Example in: {out_folder}")
    return rsl


if __name__ == "__main__":
    sys.exit(main())
