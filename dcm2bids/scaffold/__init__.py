"""scaffold module"""


import sys
import argparse
import datetime
import os
import shutil
if sys.version_info >= (3,7,0):
  import importlib.resources as resources
else:
  # backport: https://pypi.org/project/importlib-resources/
  # TODO: drop this when py3.6 is end-of-life
  import importlib_resources as resources
from ..utils import write_txt


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
        dest = os.path.join(args.output_dir, _)
        with resources.path(__name__, _) as src:
            shutil.copyfile(src, dest)

    with resources.path(__name__, "CHANGES") as changes_template:
        with open(changes_template) as _:
            data = _.read().format(datetime.date.today().strftime("%Y-%m-%d"))
        write_txt(
            os.path.join(args.output_dir, "CHANGES"),
            data.split("\n")[:-1],
    )
