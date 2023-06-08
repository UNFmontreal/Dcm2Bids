# -*- coding: utf-8 -*-

import os
import shutil


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
    def check(path):
        if os.path.isdir(path):
            if os.listdir(path):
                if not args.overwrite:
                    parser.error(
                        f"Output directory {path} isn't empty, so some files "
                        "could be overwritten or deleted.\nRerun the command"
                        " with --force option to overwrite "
                        "existing output files.")
            else:
                for the_file in os.listdir(path):
                    file_path = os.path.join(path, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(e)

    if isinstance(required, str):
        required = [required]

    for cur_dir in required:
        check(cur_dir)


def add_overwrite_arg(parser):
    parser.add_argument(
        '--force', dest='overwrite', action='store_true',
        help='Force overwriting of the output files.')
