# -*- coding: utf-8 -*-

"""helper module"""

import argparse
import os
import sys
from .dcm2niix import Dcm2niix
from .utils import DEFAULT, assert_dirs_empty

EPILOG = """
    Documentation at https://github.com/unfmontreal/Dcm2Bids
    """


def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__, epilog=EPILOG,
                                formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument("-d", "--dicom_dir",
                   required=True, nargs="+",
                   help="DICOM files directory.")

    p.add_argument("-o", "--output_dir",
                   required=False, default=DEFAULT.cliOutputDir,
                   help="Output BIDS directory."
                        " (Default: %(default)s)")

    p.add_argument('--force',
                   dest='overwrite', action='store_true',
                   help='Force command to overwrite existing output files.')

    return p


def main():
    """Let's go"""
    parser = _build_arg_parser()
    args = parser.parse_args()
    out_folder = os.path.join(args.output_dir, 'tmp_dcm2bids', 'helper')
    assert_dirs_empty(parser, args, out_folder)
    app = Dcm2niix(dicomDirs=args.dicom_dir, bidsDir=args.output_dir)
    rsl = app.run()
    print("Example in:")
    print(os.path.join(args.output_dir, DEFAULT.tmpDirName, DEFAULT.helperDir))
    return rsl


if __name__ == "__main__":
    sys.exit(main())
