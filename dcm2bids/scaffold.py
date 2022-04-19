#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Create basic BIDS files and directories
"""


import sys
import argparse
import datetime
import os
import shutil
from .utils import (DEFAULT, add_overwrite_arg, assert_dirs_empty,
                    get_scaffold_dir, write_txt)


EPILOG = DEFAULT.doc


def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__, epilog=EPILOG,
                                formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument("-o", "--output_dir",
                   required=False,
                   default=DEFAULT.cliOutputDir,
                   help="Output BIDS directory. Default: [%(default)s]")

    add_overwrite_arg(p)

    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    assert_dirs_empty(parser, args, args.output_dir)

    for _ in ["code", "derivatives", "sourcedata"]:
        os.makedirs(os.path.join(args.output_dir, _), exist_ok=True)

    scaffold_dir = get_scaffold_dir()

    for _ in os.listdir(scaffold_dir):
        dest = os.path.join(args.output_dir, _)
        src = os.path.join(scaffold_dir, _)
        shutil.copyfile(src, dest)

    changes_template = os.path.join(args.output_dir,  "CHANGES")
    with open(changes_template) as _:
        data = _.read().format(datetime.date.today().strftime("%Y-%m-%d"))

    write_txt(os.path.join(args.output_dir, "CHANGES"),
              data.split("\n")[:-1])


if __name__ == "__main__":
    sys.exit(main())
