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
dcm2bids [-h] -d DICOM_DIR -p PARTICIPANT [-s SESSION] -c CONFIG
         [--dry_dcm2niix] [-y]
```

You need to build the config file of your study to let `dcm2bids` associate your acquisitions with the right dicoms through bids sidecar created by dcm2niix. Every study is different and this step needs a little bit of work.

The configuration uses the `json` format and one example is provided in the `example` directory.

#### Descriptions

The description field is a list of dictionnary. Each dictionnary describes one acquisition.

#### Output

dcm2bids create `sub-<PARTICIPANT>` directories in the folder the script is launched.

Acquisitions with no or more than one fitting descriptions are kept in `tmp_dcm2niix` directory. Users can review these missing acquistions to change the configuration file accordingly.

[bids]: http://bids.neuroimaging.io/
[bids-spec]: http://bids.neuroimaging.io/#download
[conda]: https://conda.io/docs/
[dcm2niix-github]: https://github.com/rordenlab/dcm2niix
[dcm2niix-nitrc]: https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage
