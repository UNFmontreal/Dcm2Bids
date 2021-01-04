"""scaffold module"""


import argparse
import datetime
import os
import shutil
from ..utils import write_txt


SELF_DIR = os.path.dirname(os.path.realpath(__file__))


def _get_arguments():
    """Load arguments for main"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
            Create basic BIDS files and directories
            """,
        epilog="""
            Documentation at https://github.com/unfmontreal/Dcm2Bids
            """,
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        required=False,
        default=os.getcwd(),
        help="Output BIDS directory, Default: current directory",
    )

    args = parser.parse_args()
    return args


def scaffold():
    """scaffold entry point"""
    args = _get_arguments()

    for _ in ["code", "derivatives", "sourcedata"]:
        os.makedirs(os.path.join(args.output_dir, _), exist_ok=True)

    for _ in [
        "dataset_description.json",
        "participants.json",
        "participants.tsv",
        "README",
    ]:
        shutil.copyfile(os.path.join(SELF_DIR, _), os.path.join(args.output_dir, _))

    with open(os.path.join(SELF_DIR, "CHANGES")) as _:
        data = _.read().format(datetime.date.today().strftime("%Y-%m-%d"))
    write_txt(
        os.path.join(args.output_dir, "CHANGES"),
        data.split("\n")[:-1],
    )
