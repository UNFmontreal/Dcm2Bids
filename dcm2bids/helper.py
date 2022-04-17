# -*- coding: utf-8 -*-

"""helper module"""

import argparse
import os
import sys
from .dcm2niix import Dcm2niix
from .utils import DEFAULT, valid_path


def get_arguments():
    """Load arguments for main"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="",
        epilog="""
            Documentation at https://github.com/unfmontreal/Dcm2Bids
            """,
    )

    parser.add_argument(
        "-d", "--dicom_dir", required=True, nargs="+", help="DICOM files directory"
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        required=False,
        default=DEFAULT.cliOutputDir,
        help="Output BIDS directory, Default: current directory",
    )

    args = parser.parse_args()
    return args


def main():
    """Let's go"""
    args = get_arguments()
    valid_dicom_dir = []
    for _dir in args.dicom_dir:
        valid_dicom_dir.append(valid_path(_dir))

    app = Dcm2niix(dicomDirs=valid_dicom_dir,
                   bidsDir=valid_path(args.output_dir))
    rsl = app.run()
    print("Example in:")
    print(os.path.join(args.output_dir, DEFAULT.tmpDirName, DEFAULT.helperDir))
    return rsl


if __name__ == "__main__":
    sys.exit(main())
