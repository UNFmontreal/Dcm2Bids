---
title: Guide
---

# Introduction

dcm2bids converts one session at a time. A session is all the acquisitions between the entry and exit of the participant in the scanner.

You need to build a configuration file of your study to let dcm2bids associates your acquisitions through BIDS sidecar. Every study is different and this step needs a little bit of work. The scanner parameters should not change too much for one study (several MRI sessions), so a few configuration files should work.

BIDS sidecar<sup>1</sup> files are `JSON` files with meta informations about the acquisition. `dcm2niix` (DICOM to NIfTI converter used by dcm2bids) creates automatically one BIDS sidecar for each NIfTI file.

dcm2bids configuration file uses also the `JSON` format. One example is provided in the `example` folder on the github repository.

It is recommended to use an editor with syntax highlighting to build a correct JSON file. Here is an [online][json-editor] one.

# Usage

How to launch dcm2bids when you have build your configuration file ? First `cd` in your BIDS directory.

`dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -c CONFIG_FILE`

If your participant have a session ID:

`dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -s SESSION_ID -c CONFIG_FILE`

dcm2bids creates log files inside `tmp_dcm2bids/log`

See `dcm2bids -h` for more informations

# Configuration file example

```json
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

The `descriptions` field is a list of descriptions, each describing some acquisition. In this example, the configuration describes three acquisitions, a T2 weighted, resting state fMRI and a fieldmap.

Each description tells dcm2bids how to group a set of acquisitions and how to label them. In this config file, Dcm2Bids is being told to collect files containing

```json
{
    "SeriesDescription": "AXIAL_T2_SPACE",
    "EchoTime": 0.1
}
```

in their sidecars<sup>1</sup> and label them as `anat`, `T2w` type images.

## criteria

dcm2bids will try to match the sidecars<sup>1</sup> of dcm2niix to the descriptions of the configuration file. The values you enter inside the criteria dictionary are patterns that will be compared to the corresponding key of the sidecar.

The pattern matching is shell-style. It's possible to use wildcard `*`, single character `?` etc ... Please have a look at the [GNU documentation][gnu-pattern] to know more.

For example, in the first description, the pattern `*T2*` will be compared to the value of `SeriesDescription` of a sidecar. `AXIAL_T2_SPACE` will be a match, `AXIAL_T1` won't.

`dcm2bids` has a `SidecarFilename` key, as in the second description, if you prefer to also match with the filename of the sidecar.

You can enter several criteria. **All criteria must match** for a description to be linked to a sidecar.

## dataType

It is a mandatory field. Here is a definition from `bids v1.2.0` :

> Data type - a functional group of different types of data. In BIDS we define six data types: func (task based and resting state functional MRI), dwi (diffusion weighted imaging), fmap (field inhomogeneity mapping data such as field maps), anat (structural imaging such as T1, T2, etc.), meg (magnetoencephalography), beh (behavioral).

## modalityLabel

It is a mandatory field. It describes the modality of the acquisition like `T1w`, `T2w` or `dwi`, `bold`.

## customLabels

It is an optional field. For some acquisitions, you need to add information in the file name. For resting state fMRI, it is usally `task-rest`.

To know more on how to set these fields, read the [BIDS specifications][bids-spec].

For a longer example of a Dcm2Bids config json, see [here](https://github.com/cbedetti/Dcm2Bids/blob/master/example/config.json).

## sidecarChanges

Optional field to change or add information in a sidecar.

## intendedFor

Optional field to add an `IntendedFor` entry in the sidecar of a fieldmap. Just put the index or a list of index of the description(s) that's intended for.

Python index begins at `0` so in the example, `1` means it is intended for `task-rest_bold`.

### <sup>1</sup>: sidecars
{: .no_toc }

For each acquisition, __dcm2niix__ creates an associated .json file, containing information from the dicom header. These are known as __sidecars__. These are the sidecars __dcm2bids__ uses to filter the groups of acquisitions.

To define this filtering you will probably need to review these sidecars. You can generate all the sidecars for an individual participant using [dcm2bids_helper](#tools).

# Advanced configuration

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

## searchMethod

default: `"searchMethod": "fnmatch"`

fnmatch is the behaviour (See criteria) by default and the fall back if this option is set incorrectly. `re` is the other choice if you want more flexibility to match criteria.

## defaceTpl

default: `"defaceTpl": None`

The anonymizer option no longer exists from `v2.0.0`. It is still possible to deface the anatomical nifti images.

For example, if you use the last version of pydeface, add:

`"defaceTpl": "pydeface --outfile {dstFile} {srcFile}"`

It is a template string and dcm2bids will replace {srcFile} and {dstFile} by the source file (input) and the destination file (output).

## dcm2niixOptions

default: `"dcm2niixOptions": "-b y -ba y -z y -f '%3s_%f_%p_%t'"`

Arguments for dcm2niix

## compKeys

default: `"compKeys": ["SeriesNumber", "AcquisitionTime", "SidecarFilename"]`

Acquisitions are sorted using the sidecar data. The default behaviour is to sort by `SeriesNumber` then by `AcquisitionTime` then by the `SidecarFilename`. You can change this behaviour setting this key inside the configuration file.

# Output

dcm2bids creates a `sub-<PARTICIPANT_ID>` directory in the output directory (by default the folder where the script is launched).

Sidecars with one matching description will be convert to BIDS. If a file already exists, dcm2bids won't overwrite it. You should use the `--clobber` option to overwrite files.

If a description matches several sidecars, dcm2bids will add automatically the custom label `run-` to the filename.

Sidecars with no or more than one matching descriptions are kept in `tmp_dcm2bids` directory. Users can review these mismatches to change the configuration file accordingly.

# Tools

## Helper

`dcm2bids_helper -d DICOM_DIR [-o OUTPUT_DIR]`

To build the configuration file, you need to have a example of the sidecars. You can use `dcm2bids_helper` with the DICOMs of one participant. It will launch dcm2niix and save the result inside the `tmp_dcm2bids/helper` of the output directory.

## Scaffold

`dcm2bids_scaffold [-o OUTPUT_DIR]`

Create basic BIDS files and directories in the output directory (by default folder where the script is launched).

# bids-validator

Run the [bids-validator][bids-validator] to check your directory. Don't forget to create a `.bidsignore` file at the root of your BIDS directory with `tmp_dcm2bids/*` inside.

[bids]: http://bids.neuroimaging.io/
[bids-examples]: https://github.com/bids-standard/bids-examples
[bids-nature]: https://www.nature.com/articles/sdata201644
[bids-spec]: https://bids-specification.readthedocs.io/en/stable/
[bids-validator]: https://github.com/bids-standard/bids-validator
[dcm2bids-doc]: https://cbedetti.github.io/Dcm2Bids
[dcm2niix-github]: https://github.com/rordenlab/dcm2niix
[dcm2niix-install]: https://github.com/rordenlab/dcm2niix#install
[dcm2niix-release]: https://github.com/rordenlab/dcm2niix/releases
[gnu-pattern]: https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html
[json-editor]: http://jsoneditoronline.org/
