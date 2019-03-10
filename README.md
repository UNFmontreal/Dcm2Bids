# Dcm2Bids

Dcm2Bids reorganises NIfTI files from [dcm2niix][dcm2niix-github] into the [Brain Imaging Data Structure][bids] (BIDS).

Before using this software, learn more about BIDS:
 - read the [specifications][bids-spec]
 - a conversion [guide][bids-nature]
 - some [examples][bids-examples] datasets
 - a [validator][bids-validator] tool

## Install

#### Dependencies

- Python 2 or 3 with the `future` module, `pip` will install it automatically
- `dcm2niix` : DICOM to NIfTI conversion tool. **You need to install it**
  - [NITRC][dcm2niix-nitrc] for compiled versions
  - [Recent release][dcm2niix-release]
  - [github][dcm2niix-github] to build from source code

#### dcm2bids

###### with pip

There's several ways:

`pip install dcm2bids`

or `pip install https://github.com/cbedetti/Dcm2Bids/archive/master.zip`

or

```
git clone https://github.com/cbedetti/Dcm2Bids.git
cd Dcm2Bids
pip install .
```

Don't forget to use `--user` or `-e` flags depending on your needs. See `pip install --help` for more informations.

###### with singularity

[![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/544)

A bit overkill, but it's there.

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
            },
            "sidecarChanges": {
                "ProtocolName": "T2"
            }
        },
        {
            "dataType": "func",
            "modalityLabel": "bold",
            "customLabels": "task-rest",
            "criteria": {
                "SidecarFilename": "006*"
                "ImageType": ["ORIG*", "PRIMARY", "M", "ND", "MOSAIC"]
            }
        },
        {
            "dataType": "fmap",
            "modalityLabel": "fmap",
            "intendedFor": 1,
            "criteria": {
                "ProtocoleName": "*field_mapping*"
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

#### `sidecarChanges`

Optional field to change or add information in a sidecar.

#### `intendedFor`

Optional field to add an `IntendedFor` entry in the sidecar of a fieldmap. Just put the index of the description that's intended for. Python index begins at `0` so in the example, `1` means it is intended for `task-rest_bold`.

## Advanced configuration

These optional configurations could be insert in the configuration file at the same level as the `"descriptions"` entry.

```
{
    "searchMethod": "fnmatch",
    "defaceTpl": "pydeface --outfile {dstFile} {srcFile}",
    "description": [
        ...
    ]
}
```

#### `searchMethod`

default: `"searchMethod": "fnmatch"`

fnmatch is the behaviour (See criteria) by default and the fall back if this option is set incorrectly. `re` is the other choice if you want more flexibility to match criteria.

#### `defaceTpl`

default: `"defaceTpl": None`

The anonymizer option no longer exists from the script in this release
It is still possible to deface the anatomical nifti images
Please add "defaceTpl" key in the congifuration file

For example, if you use the last version of pydeface, add:
"defaceTpl": "pydeface --outfile {dstFile} {srcFile}"
It is a template string and dcm2bids will replace {srcFile} and {dstFile}
by the source file (input) and the destination file (output)
"pydeface --outfile {dstFile} (srcFile}",

#### `dcm2niixOptions`

default: `"dcm2niixOptions": "-b y -ba y -z y -f '%3s_%f_%p_%t'"`

Arguments for dcm2niix

#### `compKeys`

default: `"compKeys": ["SeriesNumber", "AcquisitionTime", "SidecarFilename"]`

Acquisitions are sorted using the sidecar data. The default behaviour is to sort by `SeriesNumber` then by `AcquisitionTime` then by the `SidecarFilename`. You can change this behaviour setting this key inside the configuration file.

## Output

dcm2bids creates a `sub-<PARTICIPANT ID>` directory in the output directory (by default the folder where the script is launched).

Sidecars with one matching description will be convert to BIDS. If a file already exists, dcm2bids won't overwrite it. You should use the `--clobber` option to overwrite files.

If a description matches several sidecars, dcm2bids will add automatically the custom label `run-` to the filename.

Sidecars with no or more than one matching descriptions are kept in `dcm2bids_data` directory. Users can review these mismatches to change the configuration file accordingly.

## Tools

#### Helper

`dcm2bids_helper -d DICOM_DIR [-o OUTPUT_DIR]`

To build the configuration file, you need to have a example of the sidecars. You can use `dcm2bids_helper` with the DICOMs of one participant. It will launch dcm2niix and save the result inside the `tmp_dcm2bids/helper` of the output directory.

#### Scaffold

`dcm2bids_scaffold [-o OUTPUT_DIR]`

Create basic BIDS files and directories in the output directory (by default folder where the script is launched).

## Usage

How to launch dcm2bids when you have build your configuration file ? First `cd` in your BIDS directory.

`dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -c CONFIG_FILE`

If your participant have a session ID:

`dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -s SESSION_ID -c CONFIG_FILE`

dcm2bids creates log files inside `tmp_dcm2bids/log`

See `dcm2bids -h` for more informations

## bids-validator

Run the [bids-validator][bids-validator] to check your directory. Don't forget to create a `.bidsignore` file at the root of your BIDS directory with `tmp_dcm2bids/*` inside.

## Similar projects

Other tools to create [BIDS][bids] datasets :

- [heudiconv][link-heudiconv]
- [bidskit][link-bidskit]
- [dac2bids][link-dac2bids]

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
[link-heudiconv]: https://github.com/nipy/heudiconv
[link-bidskit]: https://github.com/jmtyszka/bidskit
[link-dac2bids]: https://github.com/dangom/dac2bids
