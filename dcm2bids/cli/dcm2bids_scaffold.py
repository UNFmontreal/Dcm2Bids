#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Create basic BIDS files and directories.

    Based on the material provided by
    https://github.com/bids-standard/bids-starter-kit
"""


import argparse
import datetime
import logging
import os
import sys
from os.path import join as opj
from dcm2bids.utils.io import write_txt
from dcm2bids.utils.args import add_overwrite_arg, assert_dirs_empty
from dcm2bids.utils.utils import DEFAULT, run_shell_command, TreePrinter
from dcm2bids.utils.scaffold import bids_starter_kit
from dcm2bids.utils.logger import setup_logging


def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__, epilog=DEFAULT.doc,
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

    setup_logging("info")
    logger = logging.getLogger(__name__)

    assert_dirs_empty(parser, args, args.output_dir)

    for _ in ["code", "derivatives", "sourcedata"]:
        os.makedirs(opj(args.output_dir, _), exist_ok=True)

    logger.info("Currently running the following command: \n" +
                " ".join(sys.argv) + "\n")
    logger.info("The files used to create your BIDS directory were taken from "
                "https://github.com/bids-standard/bids-starter-kit. \n")

    # CHANGES
    write_txt(opj(args.output_dir, "CHANGES"),
              bids_starter_kit.CHANGES.replace('DATE',
                                               datetime.date.today().strftime(
                                                 "%Y-%m-%d")
                                               )
              )
    # dataset_description
    write_txt(opj(args.output_dir, "dataset_description"),
              bids_starter_kit.dataset_description.replace("BIDS_VERSION",
                                                           DEFAULT.bids_version))

    # participants.json
    write_txt(opj(args.output_dir, "participants.json"),
              bids_starter_kit.participants_json)

    # participants.tsv
    write_txt(opj(args.output_dir, "participants.tsv"),
              bids_starter_kit.participants_tsv)

    # .bidsignore
    write_txt(opj(args.output_dir, ".bidsignore"),
              "tmp_dcm2bids")

    # README
    try:
        run_shell_command(['wget', '-q', '-O', opj(args.output_dir, "README"),
                           'https://raw.githubusercontent.com/bids-standard/bids-starter-kit/main/templates/README.MD'],
                          log=False)
    except Exception:
        write_txt(opj(args.output_dir, "README"),
                  bids_starter_kit.README)

    # output tree representation of where the scaffold was built.

    TreePrinter(args.output_dir).print_tree()


if __name__ == "__main__":
    main()
