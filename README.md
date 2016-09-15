# Dcm2Bids

Dcm2Bids convert DICOM files to [Brain Imaging Data Structure][bids] (BIDS).

Learn more about BIDS and read the [specifications][bids-spec].

# Usage

1. `dcm2bids -o <BIDS dir> -d <DICOM dir> -p <participant> -a <algorithm to parse your DICOM dir>`

It's possible to add a session with the key `-s`

# DICOM directories algorithm parser

Every study is different and this step needs a little bit of work.

The logic is in `studyparser.py` and parse different part of the metadata to filter the DICOM directories.

It creates a batch file in YAML format to feed `dcm2niibatch`.

# DICOM to NIfTI conversion

Conversion is done with `dcm2niix` through `dcm2niibatch` tool. See [dcm2niix][dcm2niix] github.

# Metadata

[dcmstack][dcmstack] is used to extract metadata from DICOM files with default filtering.

IT IS YOUR RESPONSIBILITY TO KNOW IF THERE IS PRIVATE HEALTH INFORMATION IN THE METADATA EXTRACTED BY THIS PROGRAM.

# To Do

- find a more pleasant way for the user to enter algotithm
- add bids validator
- doc strings
- write test

[bids]: http://bids.neuroimaging.io/
[bids-spec]: http://bids.neuroimaging.io/#download
[dcmstack]: https://github.com/moloney/dcmstack
[dcm2niix]: https://github.com/neurolabusc/dcm2niix
