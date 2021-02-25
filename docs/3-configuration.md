# Configuration file

## Configuration file example

```json
{
    "descriptions": [
        {
            "dataType": "func",
            "modalityLabel": "bold",
            "customLabels": "task-rest",
            "criteria": {
                "SidecarFilename": "006*",
                "ImageType": ["ORIG*", "PRIMARY", "M", "ND", "MOSAIC"]
            }
        },
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
            "dataType": "fmap",
            "modalityLabel": "fmap",
            "intendedFor": 0,
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

in their sidecars[^1] and label them as `anat`, `T2w` type images.

## criteria

dcm2bids will try to match the sidecars[^1] of dcm2niix to the descriptions of the configuration file. The values you enter inside the criteria dictionary are patterns that will be compared to the corresponding key of the sidecar.

The pattern matching is shell-style. It's possible to use wildcard `*`, single character `?` etc ... Please have a look at the [GNU documentation][gnu-pattern] to know more.

For example, in the second description, the pattern `*T2*` will be compared to the value of `SeriesDescription` of a sidecar. `AXIAL_T2_SPACE` will be a match, `AXIAL_T1` won't.

`dcm2bids` has a `SidecarFilename` key, as in the first description, if you prefer to also match with the filename of the sidecar.

You can enter several criteria. **All criteria must match** for a description to be linked to a sidecar.

## dataType

It is a mandatory field. Here is a definition from `bids v1.2.0` :

> Data type - a functional group of different types of data. In BIDS we define six data types: func (task based and resting state functional MRI), dwi (diffusion weighted imaging), fmap (field inhomogeneity mapping data such as field maps), anat (structural imaging such as T1, T2, etc.), meg (magnetoencephalography), beh (behavioral).

## modalityLabel

It is a mandatory field. It describes the modality of the acquisition like `T1w`, `T2w` or `dwi`, `bold`.

## customLabels

It is an optional field. For some acquisitions, you need to add information in the file name. For resting state fMRI, it is usally `task-rest`.

To know more on how to set these fields, read the [BIDS specifications][bids-spec].

For a longer example of a Dcm2Bids config json, see [here](https://github.com/unfmontreal/Dcm2Bids/blob/master/example/config.json).

## sidecarChanges

Optional field to change or add information in a sidecar.

## intendedFor

Optional field to add an `IntendedFor` entry in the sidecar of a fieldmap. Just put the index or a list of index of the description(s) that's intended for.

Python index begins at `0` so in the example, `0` means it is intended for `task-rest_bold`.

[^1]: For each acquisition, `dcm2niix` creates an associated `.json` file,
    containing information from the dicom header. These are known as
    __sidecars__. These are the sidecars `dcm2bids` uses to filter the groups
    of acquisitions.

    To define this filtering you will probably need to review these sidecars.
    You can generate all the sidecars for an individual participant using [dcm2bids_helper](1-usage.md#tools).

[bids-spec]: https://bids-specification.readthedocs.io/en/stable/
[gnu-pattern]: https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html