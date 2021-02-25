# -*- coding: utf-8 -*-

"""dcm2bids module"""

import argparse
import logging
import os
import platform
import sys
from datetime import datetime
from glob import glob
from .dcm2niix import Dcm2niix
from .logger import setup_logging
from .sidecar import Sidecar, SidecarPairing
from .structure import Participant
from .utils import DEFAULT, load_json, save_json, run_shell_command, splitext_
from .version import __version__, check_latest, dcm2niix_version


class Dcm2bids(object):
    """ Object to handle dcm2bids execution steps

    Args:
        dicom_dir (str or list): A list of folder with dicoms to convert
        participant (str): Label of your participant
        config (path): Path to a dcm2bids configuration file
        output_dir (path): Path to the BIDS base folder
        session (str): Optional label of a session
        clobber (boolean): Overwrite file if already in BIDS folder
        forceDcm2niix (boolean): Forces a cleaning of a previous execution of
                                 dcm2niix
        log_level (str): logging level
    """

    def __init__(
        self,
        dicom_dir,
        participant,
        config,
        output_dir=DEFAULT.outputDir,
        session=DEFAULT.session,
        clobber=DEFAULT.clobber,
        forceDcm2niix=DEFAULT.forceDcm2niix,
        log_level=DEFAULT.logLevel,
        **_
    ):
        self._dicomDirs = []

        self.dicomDirs = dicom_dir
        self.bidsDir = output_dir
        self.config = load_json(config)
        self.participant = Participant(participant, session)
        self.clobber = clobber
        self.forceDcm2niix = forceDcm2niix
        self.logLevel = log_level

        # logging setup
        self.set_logger()

        self.logger.info("--- dcm2bids start ---")
        self.logger.info("OS:version: %s", platform.platform())
        self.logger.info("python:version: %s", sys.version.replace("\n", ""))
        self.logger.info("dcm2bids:version: %s", __version__)
        self.logger.info("dcm2niix:version: %s", dcm2niix_version())
        self.logger.info("participant: %s", self.participant.name)
        self.logger.info("session: %s", self.participant.session)
        self.logger.info("config: %s", os.path.realpath(config))
        self.logger.info("BIDS directory: %s", os.path.realpath(output_dir))

    @property
    def dicomDirs(self):
        """List of DICOMs directories"""
        return self._dicomDirs

    @dicomDirs.setter
    def dicomDirs(self, value):
        if isinstance(value, list):
            dicom_dirs = value
        else:
            dicom_dirs = [value]

        dir_not_found = []
        for _dir in dicom_dirs:
            if os.path.isdir(_dir):
                pass
            else:
                dir_not_found.append(_dir)

        if dir_not_found:
            raise FileNotFoundError(dir_not_found)

        self._dicomDirs = dicom_dirs

    def set_logger(self):
        """ Set a basic logger"""
        logDir = os.path.join(self.bidsDir, DEFAULT.tmpDirName, "log")
        logFile = os.path.join(
            logDir,
            "{}_{}.log".format(
                self.participant.prefix, datetime.now().isoformat().replace(":", "")
            ),
        )

        # os.makedirs(logdir, exist_ok=True)
        # python2 compatibility
        if not os.path.exists(logDir):
            os.makedirs(logDir)

        setup_logging(self.logLevel, logFile)
        self.logger = logging.getLogger(__name__)

    def run(self):
        """Run dcm2bids"""
        dcm2niix = Dcm2niix(
            self.dicomDirs,
            self.bidsDir,
            self.participant,
            self.config.get("dcm2niixOptions", DEFAULT.dcm2niixOptions),
        )
        dcm2niix.run(self.forceDcm2niix)

        sidecars = []
        for filename in dcm2niix.sidecarFiles:
            sidecars.append(
                Sidecar(filename, self.config.get("compKeys", DEFAULT.compKeys))
            )
        sidecars = sorted(sidecars)

        parser = SidecarPairing(
            sidecars,
            self.config["descriptions"],
            self.config.get("searchMethod", DEFAULT.searchMethod),
            self.config.get("caseSensitive", DEFAULT.caseSensitive)
        )
        parser.build_graph()
        parser.build_acquisitions(self.participant)
        parser.find_runs()

        self.logger.info("moving acquisitions into BIDS folder")
        for acq in parser.acquisitions:
            self.move(acq)

        check_latest()
        check_latest("dcm2niix")

    def move(self, acquisition):
        """Move an acquisition to BIDS format"""
        for srcFile in glob(acquisition.srcRoot + ".*"):
            _, ext = splitext_(srcFile)
            dstFile = os.path.join(self.bidsDir, acquisition.dstRoot + ext)

            # os.makedirs(os.path.dirname(dstFile), exist_ok=True)
            # python2 compatibility
            if not os.path.exists(os.path.dirname(dstFile)):
                os.makedirs(os.path.dirname(dstFile))

            # checking if destination file exists
            if os.path.isfile(dstFile):
                self.logger.info("'%s' already exists", dstFile)

                if self.clobber:
                    self.logger.info("Overwriting because of 'clobber' option")

                else:
                    self.logger.info("Use clobber option to overwrite")
                    continue

            # it's an anat nifti file and the user using a deface script
            if (
                self.config.get("defaceTpl")
                and acquisition.dataType == "anat"
                and ".nii" in ext
            ):
                try:
                    os.remove(dstFile)
                except FileNotFoundError:
                    pass
                defaceTpl = self.config.get("defaceTpl")
                cmd = defaceTpl.format(srcFile=srcFile, dstFile=dstFile)
                run_shell_command(cmd)

            # use
            elif ext == ".json":
                data = acquisition.dstSidecarData(self.config["descriptions"])
                save_json(dstFile, data)
                os.remove(srcFile)

            # just move
            else:
                os.rename(srcFile, dstFile)


def get_arguments():
    """Load arguments for main"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure
dcm2bids {}""".format(
            __version__
        ),
        epilog="""
            Documentation at https://github.com/unfmontreal/Dcm2Bids
            """,
    )

    parser.add_argument(
        "-d", "--dicom_dir", required=True, nargs="+", help="DICOM directory(ies)"
    )

    parser.add_argument("-p", "--participant", required=True, help="Participant ID")

    parser.add_argument(
        "-s", "--session", required=False, default=DEFAULT.cliSession, help="Session ID"
    )

    parser.add_argument(
        "-c",
        "--config",
        required=True,
        help="JSON configuration file (see example/config.json)",
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        required=False,
        default=DEFAULT.cliOutputDir,
        help="Output BIDS directory, Default: current directory ({})".format(
            DEFAULT.cliOutputDir
        ),
    )

    parser.add_argument(
        "--forceDcm2niix",
        required=False,
        action="store_true",
        help="Overwrite previous temporary dcm2niix output if it exists",
    )

    parser.add_argument(
        "--clobber",
        required=False,
        action="store_true",
        help="Overwrite output if it exists",
    )

    parser.add_argument(
        "-l",
        "--log_level",
        required=False,
        default=DEFAULT.cliLogLevel,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging level",
    )

    parser.add_argument(
        "-a",
        "--anonymizer",
        required=False,
        action="store_true",
        help="""
        This option no longer exists from the script in this release.
        See:https://github.com/unfmontreal/Dcm2Bids/blob/master/README.md#defaceTpl""",
    )

    args = parser.parse_args()
    return args


def main():
    """Let's go"""
    args = get_arguments()

    if args.anonymizer:
        print(
            """
        The anonymizer option no longer exists from the script in this release
        It is still possible to deface the anatomical nifti images
        Please add "defaceTpl" key in the congifuration file

        For example, if you use the last version of pydeface, add:
        "defaceTpl": "pydeface --outfile {dstFile} {srcFile}"
        It is a template string and dcm2bids will replace {srcFile} and {dstFile}
        by the source file (input) and the destination file (output)
        """
        )
        return 1

    app = Dcm2bids(**vars(args))
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
