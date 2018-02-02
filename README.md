# Dcm2Bids

Dcm2Bids reorganises NIfTI files from [dcm2niix][dcm2niix-github] into the [Brain Imaging Data Structure][bids] (BIDS).

Before using this software, learn more about BIDS:
 - read the [specifications][bids-spec]
 - a conversion [guide][bids-nature]
 - some [examples][bids-examples] datasets
 - a [validator][bids-validator] tool

## Install

#### Dependencies

- Python 2 or 3 with the `future` module
- `dcm2niix` : DICOM to NIfTI conversion tool
  - [NITRC][dcm2niix-nitrc] for compiled versions
  - [Recent release][dcm2niix-release]
  - [github][dcm2niix-github] to build from source code

#### dcm2bids

###### with pip

`pip install dcm2bids`

###### from github

```
git clone https://github.com/cbedetti/Dcm2Bids.git
cd Dcm2Bids
pip install .
```

###### with singularity

TBA

## Introduction

dcm2bids converts one session at a time. A session is all the acquisitions between the entry and exit of the participant in the scanner.

You need to build a configuration file of your study to let `dcm2bids` associates your acquisitions through BIDS sidecar. Every study is different and this step needs a little bit of work. The scanner parameters should not change for one study (several MRI sessions), so one configuration file should work.

BIDS sidecar files are `JSON` files with meta informations about the acquisition. dcm2niix creates automatically one BIDS sidecar for each NIfTI file.

dcm2bids configuration file uses also the `JSON` format. One example is provided in the `example` directory.

It is recommended to use an editor with syntax highlighting to build a correct JSON file. Here is an [online][json-editor] one.

## Configuration file example

```
{
    "descriptions": [
        {
            "dataType": "anat",
            "modalityLabel": "T2w",
            "criteria": {
                "SeriesDescription": "*T2*",
                "EchoTime": 0.1
            }
        },
        {
            "dataType": "func",
            "modalityLabel": "bold",
            "customLabels": "task-rest",
            "criteria": {
                "SidecarFilename": "006*"
            }
        }
    ]
}
```

The `descriptions` field is a list of description, each describing some acquisition. In this example, the configuration describes two acquisitions, a T2 weigthed and resting state fMRI.

#### `dataType`

It is a mandatory field. Here is a definition from `bids_specs1.0.2` pdf:

> A functional group of different types of MRI data. In BIDS we define four data types: func (task based and resting state functional MRI), dwi (diffusion weighted imaging), fmap (field inhomogeneity mapping data such as field maps), anat (structural imaging such as T1, T2, etc.)

#### `modalityLabel`

It is a mandatory field. It describes the modality of the acquisition like `T1w`, `T2w` or `bold`.

#### `customLabels`

It is an optional field. For some acquisitions, you need to add information in the file name. For resting state fMRI, it is usally `task-rest`.

To know more on how to set these fields, read the [BIDS specifications][bids-spec].

#### `criteria`

dcm2bids will try to match the sidecars of dcm2niix to the descriptions of the configuration file. The values you enter inside the criteria dictionnary are patterns. They will be compared to the corresponding key of the sidecar.

The pattern matching is shell-style. It's possible to use wildcard `*`, single character `?` etc ... Please have a look at the [GNU documentation][gnu-pattern] to know more.

For example, in the first description, the pattern `*T2*` will be compared to the value of `SeriesDescription` of a sidecar. `AXIAL_T2_SPACE` will be a match, `AXIAL_T1` won't.

`dcm2bids` create a `SidecarFilename` key if you prefer to also match with the filename of the sidecar.

You can enter several criteria. **All criteria must match** for a description to be link to a sidecar.

## Output

dcm2bids creates a `sub-<PARTICIPANT ID>` directory in the output directory (by default the folder where the script is launched).

Sidecars with one matching description will be convert to BIDS. If a file already exists, dcm2bids won't overwrite it. You should use the `--clobber` option to overwrite files.

If a description matches several sidecars, dcm2bids will add automatically the custom label `run-` to the filename.

Sidecars with no or more than one matching descriptions are kept in `dcm2bids_data` directory. Users can review these mismatches to change the configuration file accordingly.

## Tools

#### Helper

`dcm2bids_helper -d DICOM_DIR [-o OUTPUT_DIR]`

To build the configuration file, you need to have a example of the sidecars. You can use `dcm2bids_helper` with the DICOMs of one participant. It will launch dcm2niix and save the result inside the `dcm2bids_data/helper` of the output directory.

#### Scaffold

`dcm2bids_scaffold [-o OUTPUT_DIR]`

Create basic BIDS files and directories in the output directory (by default folder where the script is launched).

## Usage

How to launch dcm2bids when you have build your configuration file ? First `cd` in your BIDS directory.

`dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -c CONFIG_FILE`

If your participant have a session ID:

`dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -s SESSION_ID -c CONFIG_FILE`

See `dcm2bids -h` for more informations

[bids]: http://bids.neuroimaging.io/
[bids-examples]: https://github.com/INCF/BIDS-examples
[bids-nature]: https://www.nature.com/articles/sdata201644
[bids-spec]: http://bids.neuroimaging.io/#download
[bids-validator]: https://github.com/INCF/bids-validator
[conda]: https://conda.io/docs/
[dcm2niix-github]: https://github.com/rordenlab/dcm2niix
[dcm2niix-release]: https://github.com/rordenlab/dcm2niix/releases
[dcm2niix-nitrc]: https://www.nitrc.org/frs/?group_id=889
[gnu-pattern]: https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html
[json-editor]: http://jsoneditoronline.org/
