# Advanced configuration and commands

## How to use advanced configuration

These optional configurations can be inserted in the configuration file at the
same level as the `"description"` entry.

```json
{
  "extractors": {
    "SeriesDescription": [
      "run-(?P<run>[0-9]+)",
      "task-(?P<task>[0-9]+)"
    ],
    "BodyPartExamined": [
      "(?P<bodypart>[a-zA-Z]+)"
    ]
  },
  "search_method": "fnmatch",
  "case_sensitive": true,
  "dup_method": "dup",
  "post_op": [
    {
      "cmd": "pydeface --outfile dst_file src_file",
      "datatype": "anat",
      "suffix": [
        "T1w",
        "MP2RAGE"
      ],
    "custom_entities": "rec-defaced"
    }
  ],
  "descriptions": [
    {
      "datatype": "anat",
      "suffix": "T2w",
      "custom_entities": [
        "acq-highres",
        "bodypart",
        "run",
        "task"
      ],
      "criteria": ...
    }
  ]
}
```

### `custom_entities` combined with extractors

default: None

extractors will allow you to extract information embedded into sidecar files. In
the example above, it will try to match 2 different regex expressions (keys:
task, run) within the SeriesDescription field and bodypart in BodyPartExamined
field.

By using the same keys in custom_entities and if found, it will add this new
entities directly into the final filename. custom_entities can be a list that
combined extractor keys and regular entities. If key is `task` it will
automatically add the field "TaskName" inside the sidecase file.

### `search_method`

default: `"search_method": "fnmatch"`

fnmatch is the behaviour (See criteria) by default and the fall back if this
option is set incorrectly. `re` is the other choice if you want more flexibility
to match criteria.

### `dup_method`

default: `"dup_method": "run"`

run is the default behavior and will add '\_run-' to the customEntities of the
acquisition if it finds duplicate destination roots.

dup will keep the last duplicate description and put `_dup-`to the
customEntities of the other acquisitions. This behavior is a
[heudiconv](https://heudiconv.readthedocs.io/en/latest/changes.html) inspired
feature.

### `case_sensitive`

default: `"case_sensitive": "true"`

If false, comparisons between strings/lists will be not case sensitive. It's
only disabled when used with `"search_method": "fnmatch"`.

### `post_op`

default: `"post_op": []`

post_op key allows you to run any post-processing analyses just before moving
the images to their respective directories.

For example, if you want to deface your T1w images you could use pydeface by
adding:

```json
"post_op": [
  {
    "cmd": "pydeface --outfile dst_file src_file",
    "datatype": "anat",
    "suffix": [
      "T1w",
      "MP2RAGE"
    ],
    "custom_entities": "rec-defaced"
  }
],
```

It will specifically run the corresponding `cmd` to any image that follow the
combinations datatype/suffix: `(anat, T1w) or (anat, MP2RAGE)`.

!!! warning "How to use custom_entities"

    If you want to keep both versions of the same file (for example defaced and not defaced) you need to provide extra custom_entities
    otherwise it will keep only your script output.

!!! warning "Multiple post_op commands"

    Although you can add multiple commands, the combination datatype/suffix on which you want to run the command has to be unique.
    You cannot run multiple commands on a specific combination datatype/suffix.

```json
"post_op": [{"cmd": "pydeface --outfile dst_file src_file",
            "datatype": "anat",
            "suffix": ["T1w", "MP2RAGE"],
            "custom_entities": "rec-defaced"},
            {"cmd": "my_new_script --input src_file --output dst_file ",
            "datatype": "fmap",
            "suffix": ["any"]}],
```

In this example the second command `my_new_script` will be running on any image
which datatype is fmap.

Finally, this is a template string and dcm2bids will replace `src_file` and
`dst_file` by the source file (input) and the destination file (output).

### `dcm2niixOptions`

default: `"dcm2niixOptions": "-b y -ba y -z y -f '%3s_%f_%p_%t'"`

Arguments for dcm2niix

### `compKeys`

default: `"compKeys": ["SeriesNumber", "AcquisitionTime", "SidecarFilename"]`

Acquisitions are sorted using the sidecar data. The default behaviour is to sort
by `SeriesNumber` then by `AcquisitionTime` then by the `SidecarFilename`. You
can change this behaviour setting this key inside the configuration file.

### `criteria`

#### Handle multi site filtering

As mentioned in the [first-steps tutorial](../tutorial/first-steps.md),
criteria is the way to filter specific acquisitions. If you work with dicoms
from multiple sites you will need different criteria for the same kind of
acquisition. In order to reduce the length of the config file, we developed a
feature where for a specific criteria you can get multiple descriptions.

```json
"criteria": {
    "SeriesDescription": {"any" : ["*MPRAGE*", "*T1w*"]}
}
```

#### Enhanced float/int comparison

Criteria can help you filter acquisitions by comparing float/int sidecar.

```json
"criteria": {
    "RepetitionTime": {
        "le": "0.0086"
    }
}
```

In this example, dcm2bids will check if RepetitionTime is lower or equal to
0.0086.

Here are the key coded to help you compare float/int sidecar.

|    key     |         operator         |
| :--------: | :----------------------: |
|  **`lt`**  |        lower than        |
|  **`le`**  |  lower than or equal to  |
|  **`gt`**  |       greater than       |
|  **`ge`**  | greater than or equal to |
| **`btw`**  |         between          |
| **`btwe`** |   between or equal to    |

If you want to use btw or btwe you will need to give an ordered list like this.

```json
"criteria": {
    "EchoTime": {
        "btwe": ["0.0029", "0.003"]
    }
}
```

## How to use advanced commands

### dcm2bids advanced options

By now, you should be used to getting the `--help` information before running a
command.

=== "Command"

    ```sh
    dcm2bids --help
    ```

=== "Output"

    ```sh
    --8<-- "docs_helper/help.txt"
    ```

### `--auto_extract_entities`

This option will automatically try to find 3 entities (task, dir and echo) for
specific datatype/suffix.

- `task` in the SeriesDescription field

  Regular expression `task-(?P<task>[a-zA-Z0-9]+)`

- `dir` in the PhaseEncodedDirection field

  Regular expression `(?P<dir>-?j|i)`

- `echo` in the EchoNumber field

  Regular expression `(?P<echo>[0-9])`

If found, it will try to feed the filename with this entity **if they are
mandatory**.

For example, a "pepolar" fieldmap data requires the entity `dir` (See
[BIDS specification](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#case-4-multiple-phase-encoded-directions-pepolar)).
If you set this parameter, it will automatically try to find this entity and add
it to the filename.

So far and accordingly to the BIDS specification 5 datatype/suffix automatically
look for this 3 entities.

| datatype | suffix | Entities |
| :------: | :----: | :------: |
|   anat   | MEGRE  |   echo   |
|   anat   |  MESE  |   echo   |
|   func   |  cbv   |   task   |
|   func   |  bold  |   task   |
|   func   | sbref  |   task   |
|   fmap   |  epi   |   dir    |

Using the `--auto_extract_entitie`, if you want another combination of
datatype/suffix to be able to extract one or more of these 3 entities you need
to add the key of the entities needed using the field custom_entities like this
within your description:

```json
"custom_entities": ["echo", "dir"]
```

:warning: If task is found, it will automatically add the field `TaskName` into
the sidecar file. It means you don't have to add the field in the config file
like this.

<strike>

```json
{
  "sidecar_changes": {
    "TaskName": "learning"
  }
}
```

</strike>
   
:radioactive: You can find more detailed information by looking at the file [`dcm2bids/utils/utils.py`](../dcm2bids/utils/utils/) and
more specifically *`auto_extractors`* and *`auto_entities`* variables.

!!! danger "You cannot use `--auto_extract_entities` in conjunction with `--do_not_reorder_entities`"
    Refer to the [Manuel ordering](../create-config-file/#custom_entities) section for more information.

### `--bids_validate`

By default, dcm2bids will not validate your final BIDS structure. If needed, you
can install
[bids-validator](https://github.com/bids-standard/bids-validator#quickstart) and
activate this option.

### `--skip_dcm2niix`

If you don't have access to original dicom files you can still use dcm2bids to reorganise your data into a BIDS structure.
Using the option --skip_dcm2niix you will skip the conversion step.
