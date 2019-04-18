---
title: Advanced configuration
---

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

## participant and session

There are two ways to give the participant `<PARTICIPANT_ID>` and session `<SESSION_ID>`:

1. Through the command line using the arguments `-p` and `-s`
2. Through the config file, using a specific sidecar and a REGEX expression to grab the exact string.

```
 "participant": {
    "dcmTag": "PatientName",
    "expression": "[0-9a-zA-Z]*_sub-([0-9a-zA-Z]*)_sess-[0-9a-zA-Z]*"
    },
"session": {
    "dcmTag": "PatientName",
    "expression": "[0-9a-zA-Z]*_sub-[0-9a-zA-Z]*_sess-([0-9a-zA-Z]*)"
    }
```

**WARNING**: if you choose a sidecar that will be removed because of anonymisation you need to use this dcm2niix option: `"dcm2niixOptions": "-b y -ba n -z y -f '%3s_%f_%p_%t'"`
