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

## duplicateMethod

default: `"duplicateMethod": "run"`

When dcm2bids found duplicates, it will add `run` as a suffix by default.

If `"duplicateMethod": "dup"`, dcm2bids will behave as heudiconv (See [documentation](https://heudiconv.readthedocs.io/en/latest/changes.html#id8))

## dcmTagLabel

default: `"dcmTagLabel": "None"`

Instead of using `customLabel` and add tasks or runs for each of your acquisition, you can have a generic customLabel using `dcmTagLabel`. You need two keys within `dcmTagLabel`.

1. `dcmTag` tells dcm2bids which dicom tag you want the generic custom label to look at.
2. `expression` is one or multiple regex expression (here: tasks and runs) used to grab the different custom labels for all your acquisitions.
3. Finally, you only need to filter your acquisitions with something more generic `*task*` instead of `*task-memory*`.


```
"dcmTagLabel": {
		"dcmTag": "SeriesDescription",
		"expression": [".*(task-[0-9a-zA-Z]*).*",
			       ".*(run-[0-9]*).*"]
                },
"descriptions": [
        {
            "dataType": "func",
            "modalityLabel": "bold",
            "criteria": {
                "SeriesDescription": "*task*"
            }
        }
```

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
