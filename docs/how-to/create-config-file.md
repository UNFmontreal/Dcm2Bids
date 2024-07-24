# How to create a configuration file

## Configuration file example

```json
{
  "descriptions": [
    {
      "datatype": "anat",
      "suffix": "T2w",
      "criteria": {
        "SeriesDescription": "*T2*",
        "EchoTime": 0.1
      },
      "sidecar_changes": {
        "ProtocolName": "T2"
      }
    },
    {
      "id": "task_rest",
      "datatype": "func",
      "suffix": "bold",
      "custom_entities": "task-rest",
      "criteria": {
        "ProtocolName": "func_task-*",
        "ImageType": ["ORIG*", "PRIMARY", "M", "MB", "ND", "MOSAIC"]
      }
    },
    {
      "datatype": "fmap",
      "suffix": "fmap",
      "criteria": {
        "ProtocolName": "*field_mapping*"
      },
      "sidecar_changes": {
        "IntendedFor": "task_rest"
      }
    },
    {
      "id": "id_task_learning",
      "datatype": "func",
      "suffix": "bold",
      "custom_entities": "task-learning",
      "criteria": {
        "SeriesDescription": "bold_task-learning"
      },
      "sidecar_changes": {
        "TaskName": "learning"
      }
    },
    {
      "datatype": "fmap",
      "suffix": "epi",
      "criteria": {
        "SeriesDescription": "fmap_task-learning"
      },
      "sidecar_changes": {
        "TaskName": "learning",
        "IntendedFor": "id_task_learning"
      }
    }
  ]
}
```

The `descriptions` field is a list of descriptions, each describing some
acquisition. In this example, the configuration describes five acquisitions, a
T2-weighted, a resting-state fMRI, a fieldmap, and an fMRI learning task with
another fieldmap.

Each description tells dcm2bids how to group a set of acquisitions and how to
label them. In this config file, Dcm2Bids is being told to collect files
containing

```json
{
  "SeriesDescription": "AXIAL_T2_SPACE",
  "EchoTime": 0.1
}
```

in their sidecars[^1] and label them as `anat`, `T2w` type images.

## criteria

dcm2bids will try to match the sidecars[^1] of dcm2niix to the descriptions of
the configuration file. The values you enter inside the criteria dictionary are
patterns that will be compared to the corresponding key of the sidecar.

The pattern matching is shell-style. It's possible to use wildcard `*`, single
character `?` etc ... Please have a look at the [GNU documentation][gnu-pattern]
to know more.

For example, in the second description, the pattern `*T2*` will be compared to
the value of `SeriesDescription` of a sidecar. `AXIAL_T2_SPACE` will be a match,
`AXIAL_T1` won't.

`dcm2bids` has a `SidecarFilename` key, as in the first description, if you
prefer to also match with the filename of the sidecar. Note that filename are
subject to change depending on the dcm2niix version in use.

You can enter several criteria. **All criteria must match** for a description to
be linked to a sidecar.

## datatype

It is a mandatory field. Here is a definition from `bids v1.2.0` :

> Data type - a functional group of different types of data. In BIDS we define
> six data types: func (task based and resting state functional MRI), dwi
> (diffusion weighted imaging), fmap (field inhomogeneity mapping data such as
> field maps), anat (structural imaging such as T1, T2, etc.), meg
> (magnetoencephalography), beh (behavioral).

## suffix

It is a mandatory field. It describes the modality of the acquisition like
`T1w`, `T2w` or `dwi`, `bold`.

## custom_entities

It is an optional field. For some acquisitions, you need to add information in
the file name. For resting state fMRI, it is usually `task-rest`.

To know more on how to set these fields, read the [BIDS
specifications][bids-spec].

For a longer example of a Dcm2Bids config json, see
[here](https://github.com/unfmontreal/Dcm2Bids/blob/master/example/config.json).


Note that the different BIDS entities have a specific order to be considered valid filenames, as specified in the [Entity table of the BIDS Specification](https://bids-specification.readthedocs.io/en/stable/appendices/entity-table.html). If the custom_entities fields are entered in a different order, dcm2bids will automatically reorder them for you.

For example if you entered:

```json
"custom_entities": "run-01_task-rest"
```

when running dcm2bids, you will get the following warning:

```bash
WARNING:dcm2bids.structure:✅ Filename was reordered according to BIDS entity table order:
                from:   sub-ID01_run-01_task-rest_bold
                to:     sub-ID01_task-rest_run-01_bold
```

custom_entities could also be combined with extractors. See
[custom_entities combined with extractors](./use-advanced-commands.md#custom_entities-combined-with-extractors)

### Manuel ordering

!!! tip "`--do_not_reorder_entities`"

    If you prefer to have manual control over the order of `custom_entities`, you can use the `--do_not_reorder_entities` flag. This flag allows you to keep the order defined by you, the user, in the `custom_entities` field. However, please note that this flag cannot be used in conjunction with the `--auto_extract_entities` flag.

## sidecar_changes, id and IntendedFor

Optional field to change or add information in a sidecar.

:warning: `IntendedFor` is now considered a sidecar_changes.

Example:

```json
{
  "sidecar_changes": {
    "IntendedFor": "task_rest"
  }
}
```

If you want to add an `IntendedFor` entry or any extra sidecar linked to a
specific file, you will need to set an id to the corresponding description and
put the same id with `IntendedFor`.

For example, **`task_rest`** means it is intended for `task-rest_bold` and
**`id_task_learning`** is intended for `task-learning_bold`.

You could also use this feature to feed sidecar such as `Source`` for example or
anything that suits your needs.

## Multiple config files

It is possible to create multiple config files and iterate the `dcm2bids`
command over the different config files to structure data that have different
parameters in their sidecar files.

[^1]:
    For each acquisition, `dcm2niix` creates an associated `.json` file,
    containing information from the dicom header. These are known as
    **sidecars**. These are the sidecars that `dcm2bids` uses to filter the
    groups of acquisitions.

    To define the filters you need, you will probably have to review these
    sidecars. You can generate all the sidecars for an individual participant
    using the [dcm2bids_helper](./use-main-commands.md#tools) command.

[bids-spec]: https://bids-specification.readthedocs.io/en/stable/
[gnu-pattern]:
  https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html
