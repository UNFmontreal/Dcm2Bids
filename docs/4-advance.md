# Advanced configuration

These optional configurations could be insert in the configuration file at the same level as the `"descriptions"` entry.

```
{
    "searchMethod": "fnmatch",
    "deface": true,
    "description": [
        ...
    ]
}
```

## searchMethod

default: `"searchMethod": "fnmatch"`

fnmatch is the behaviour (See criteria) by default and the fall back if this option is set incorrectly. `re` is the other choice if you want more flexibility to match criteria.

## deface

default: `"deface": False`

To anonymize images with `pydeface`, set this to `True`.

## dcm2niixOptions

default: `"dcm2niixOptions": "-b y -ba y -z y -f '%3s_%f_%p_%t'"`

Arguments for dcm2niix

## compKeys

default: `"compKeys": ["SeriesNumber", "AcquisitionTime", "SidecarFilename"]`

Acquisitions are sorted using the sidecar data. The default behaviour is to sort by `SeriesNumber` then by `AcquisitionTime` then by the `SidecarFilename`. You can change this behaviour setting this key inside the configuration file.
