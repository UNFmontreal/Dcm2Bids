# Dcm2Bids

Dcm2Bids helps you to convert DICOM files of a study to [Brain Imaging Data Structure][bids] (BIDS).

Learn more about BIDS and read the [specifications][bids-spec].

## Install

```
git clone https://github.com/cbedetti/Dcm2Bids
```

Add the installation directory to your PYTHONPATH and the `scripts` directory to your PATH.

#### Software dependencies

- dcm2niix

DICOM to NIfTI conversion is done with `dcm2niix` converter. See their [github][dcm2niix-github] for source or [NITRC][dcm2niix-nitrc] for compiled versions.

## Usage

```
usage: dcm2bids [-h] -d DICOM_DIR [DICOM_DIR ...] -p PARTICIPANT -c CONFIG
                [-s SESSION] [--clobber] [-n SELECTSERIES [SELECTSERIES ...]]
                [-o OUTPUTDIR]

optional arguments:
  -h, --help            show this help message and exit
  -d DICOM_DIR [DICOM_DIR ...], --dicom_dir DICOM_DIR [DICOM_DIR ...]
                        DICOM files directory(ies). Wild cards are supported.
  -p PARTICIPANT, --participant PARTICIPANT
                        Participant number in BIDS output
  -c CONFIG, --config CONFIG
                        JSON configuration file (see example/config.json)
  -s SESSION, --session SESSION
                        Session name/number
  --clobber             Overwrite output if it exists
  -n SELECTSERIES [SELECTSERIES ...], --selectseries SELECTSERIES [SELECTSERIES ...]
                        Select subset of series numbers (integers) for
                        conversion
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        Output BIDS study directory (default current
                        directory)
```

#### Descriptions

The description field is a list of dictionnary. Each dictionnary describes one acquisition.

#### Output

dcm2bids creates `sub-<PARTICIPANT>` directories in the output directory (by
default the folder where the script is launched).

Acquisitions with no or more than one fitting descriptions are kept in `tmp_dcm2niix` directory. Users can review these missing acquistions to change the configuration file accordingly.

[bids]: http://bids.neuroimaging.io/
[bids-spec]: http://bids.neuroimaging.io/#download
[conda]: https://conda.io/docs/
[dcm2niix-github]: https://github.com/rordenlab/dcm2niix
[dcm2niix-nitrc]: https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage
