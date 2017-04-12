# Dcm2Bids

Dcm2Bids helps you to convert DICOM files of a study to [Brain Imaging Data Structure][bids] (BIDS).

Learn more about BIDS and read the [specifications][bids-spec].

# Install

```
git clone https://github.com/cbedetti/Dcm2Bids
```

Add the installation directory to your PYTHONPATH and the `scripts` directory to your PATH.

### Software dependencies

- [dcm2niix][dcm2niix-github] with `dcm2niibatch` compiled

### Python dependencies

The file `environment.yml` contains the python dependencies. It's possible to create a `dcm2bids` python environment with [conda][conda].

```
conda config --add channels conda-forge
conda env create -f environment.yml
```

# Usage

```
dcm2bids [-h] -o BIDS_DIR -d DICOM_DIR -p PARTICIPANT [-s SESSION] -c CONFIG [-n]
```

You need to build the config file of your study to let `dcm2bids` associate your acquisitions with the right dicoms through dicom header fields. Every study is different and this step needs a little bit of work.

The configuration uses the `json` format and one example is provided in the `example` directory.

### batch options

```
{
    "batch_options": {
        "isGz": true,
        "isFlipY": false,
        "isVerbose": false,
        "isCreateBIDS": true,
        "isOnlySingleFile": false
    }
}
```

This is the options needed for `dcm2niibatch`. Keep them like that.

### descriptions

The description field is a list of dictionnary. Each dictionnary describes one acquisition.

# Output

The script creates a batch file and save it in the `code` directory of your BIDS folder. It execute automatically `dcm2niibatch` after that. It is possible to do a dry run if you add the option `-n`.

# DICOM to NIfTI conversion

Conversion is done with `dcm2niibatch`, a tool from dcm2niix converter. See their [github][dcm2niix-github] for source or [NITRC][dcm2niix-nitrc] for compiled versions.


[bids]: http://bids.neuroimaging.io/
[bids-spec]: http://bids.neuroimaging.io/#download
[conda]: https://conda.io/docs/
[dcm2niix-github]: https://github.com/rordenlab/dcm2niix
[dcm2niix-nitrc]: https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage
