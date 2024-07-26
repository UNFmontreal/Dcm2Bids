# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
import os


def assert_dirs_empty(parser, args, required):
    """
    Assert that all directories exist are empty.
    If dirs exist and not empty, and --force is used, delete dirs.

    Parameters
    ----------
    parser: argparse.ArgumentParser object
        Parser.
    args: argparse namespace
        Argument list.
    required: string or list of paths to files
        Required paths to be checked.
    """
    def check(path: Path):
        if path.is_dir():
            if any(path.iterdir()):
                if not args.overwrite:
                    parser.error(
                        f"Output directory {path}{os.sep} isn't empty, so some files "
                        "could be overwritten or deleted.\nRerun the command "
                        "with --force option to overwrite "
                        "existing output files.")
                else:
                    for child in path.iterdir():
                        if child.is_file():
                            os.remove(child)
                        elif child.is_dir():
                            shutil.rmtree(child)

    if isinstance(required, str):
        required = Path(required)

    for cur_dir in [required]:
        check(cur_dir)


def add_overwrite_arg(parser):
    parser.add_argument(
        '--force', dest='overwrite', action='store_true',
        help='Force overwriting of the output files.')
