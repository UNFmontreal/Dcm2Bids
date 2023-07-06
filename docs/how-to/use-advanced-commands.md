# How to use advanced configuration

These optional configurations could be insert in the configuration file at the
same level as the `"descriptions"` entry.

```
{
    "extractors": {"SeriesDescription": ["run-(?P<run>[0-9]+)", "task-(?P<task>[0-9]+)"], 
                   "BodyPartExamined": ["(?P<bodypart>[a-zA-Z]+)"]},
    "search_method": "fnmatch",
    "case_sensitive": true,
    "dup_method": "dup",
    "post_op": [{"cmd": "pydeface --outfile dstFile srcFile",
               "datatype": "anat",
               "suffix": ["T1w", "MP2RAGE"]}],
    "description": [
    {
      "datatype": "anat",
      "suffix": "T2w",
      "custom_entities": ["acq-highres", "bodypart", "run", "task"],
      "criteria" : ...
    }
    ]
    ...
}
```

## custom_entities combined with extractors

default: None

extractors will allow you to extract information embeded into sidecar files. 
In the example above, it will try to match 2 different regex expressions (keys: task, run) within the 
SeriesDescription field and bodypart in BodyPartExamined field.

By using the same keys in custom_entities and if found, it will add this new entities directly into the final filename.
custom_entities can be a list that combined extractor keys and regular entities. 
If key is `task` it will automatically add the field "TaskName" inside the sidecase file.

## search_method

default: `"search_method": "fnmatch"`

fnmatch is the behaviour (See criteria) by default and the fall back if this
option is set incorrectly. `re` is the other choice if you want more flexibility
to match criteria.

## dup_method

default: `"dup_method": "run"`

run is the default behavior and will add '_run-' to the customEntities of the acquisition
if it finds duplicate destination roots.

dup will keep the last duplicate description and put `_dup-`to the customEntities of the other acquisitions.
This behavior is a [heudiconv](https://heudiconv.readthedocs.io/en/latest/changes.html) inspired feature.


## case_sensitive

default: `"case_sensitive": "true"`

If false, comparisons between strings/lists will be not case sensitive. It's
only disabled when used with `"search_method": "fnmatch"`.

## post_op

default: `"post_op": []`

post_op key allows you to run any post-processing analyses just before being moved 
to there respective folders. 

For example, if you want to deface your T1w images you could use pydeface by adding:
```
    "post_op": [{"cmd": "pydeface --outfile dstFile srcFile",
               "datatype": "anat",
               "suffix": ["T1w", "MP2RAGE"]}],
```

It will specifically run the corresponding `cmd` to any image that follow the combinations
datatype/suffix: `(anat, T1w) or (anat, MP2RAGE)`.

!!! warning "Multiple post_op commands"

    Although you can add multiple commands, the combination datatype/suffix on which you want to run the command has to be unique.
    You cannot run multiple commands on a specific combination datatype/suffix.

```
    "post_op": [{"cmd": "pydeface --outfile dstFile srcFile",
               "datatype": "anat",
               "suffix": ["T1w", "MP2RAGE"]},
               {"cmd": "my_new_script --input srcFile --output dstFile ",
               "datatype": "fmap",
               "suffix": ["any"]}],
```

In this example the second command "my_new_script" will be running on any image which datatype is fmap.

Finally, this is a template string and dcm2bids will replace srcFile and dstFile by the
source file (input) and the destination file (output).

## dcm2niixOptions

default: `"dcm2niixOptions": "-b y -ba y -z y -f '%3s_%f_%p_%t'"`

Arguments for dcm2niix

## compKeys

default: `"compKeys": ["SeriesNumber", "AcquisitionTime", "SidecarFilename"]`

Acquisitions are sorted using the sidecar data. The default behaviour is to sort
by `SeriesNumber` then by `AcquisitionTime` then by the `SidecarFilename`. You
can change this behaviour setting this key inside the configuration file.

## criteria

As mentionned in the tutorial, criteria is the way to filter specific acquisitions. If you work with dicoms from multiple sites
you will need different criterias for the same kind of acquisition. In order to reduce the length of the config file, 
we developped a feature where for a specific criteria you can get multiple descriptions. 

```
      "criteria": {
        "SeriesDescription": {"any" : ["*MPRAGE*", "*T1w*"]}
      }
```

# How to use advanced commands

## dcm2bids advanced options

By now, you should be used to getting the `--help` information before running a
command.

=== "Command"

    ```sh
    dcm2bids --help
    ```

=== "Output"

    ```sh hl_lines="2-3"
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ dcm2bids --help
    usage: dcm2bids [-h] -d DICOM_DIR [DICOM_DIR ...] -p PARTICIPANT [-s SESSION] -c CONFIG [-o OUTPUT_DIR]
                    [--auto_extract_entities] [--bids_validate] [--forceDcm2niix] [--clobber]
                    [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-a]

    Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure
    dcm2bids 3.0.0

    options:
    -h, --help            show this help message and exit
    -d DICOM_DIR [DICOM_DIR ...], --dicom_dir DICOM_DIR [DICOM_DIR ...]
                            DICOM directory(ies)
    -p PARTICIPANT, --participant PARTICIPANT
                            Participant ID
    -s SESSION, --session SESSION
                            Session ID
    -c CONFIG, --config CONFIG
                            JSON configuration file (see example/config.json)
    -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            Output BIDS directory, Default: current directory (/home/sam/dcm2bids-tutorial/bids_project)
    --auto_extract_entities If set, it will automatically try to extract entity information [task, dir, echo]
                            depending on the suffix and datatype. [False]
    --bids_validate       If set, once your conversion is done it will check if your output folder is BIDS valid. [False]
                          bids-validator needs to be installed check: https://github.com/bids-standard/bids-validator#quickstart
    --forceDcm2niix       Overwrite previous temporary dcm2niix output if it exists
    --clobber             Overwrite output if it exists
    -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                            Set logging level

                Documentation at https://github.com/unfmontreal/Dcm2Bids

    ```

## --auto_extract_entities

This option will automatically try to find 3 entities (task, dir and echo) for specific datatype/suffix.

* `task` in the SeriesDescription field

    Regex expression `task-(?P<task>[a-zA-Z0-9]+)`

* `dir` in the PhaseEncodedDirection field

    Regex expression `(?P<dir>-?j|i)`

* `echo` in the EchoNumber field 

    Regex expression `(?P<echo>[0-9])`

If found, it will try to feed the filename with this entity if they are mandatory.

For example, a "pepolar" fieldmap data requires the entity `dir` (See [BIDS specification](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#case-4-multiple-phase-encoded-directions-pepolar)). 
If you set this parameter, it will automatically try to find this entity and add it to the filename.

So far and accordingly to the BIDS specification 5 datatype/suffix automatically look for this 3 entities.

| datatype |  suffix | Entities |
|:--------:|:----------:|:--------:|
| anat | MEGRE | echo |
| anat | MESE | echo |
| func | cbv | task |
| func | bold | task |
| func | sbref | task |
| fmap | epi | dir |

Using the `--auto_extract_entitie`, if you want another combination of datatype/suffix to be able to 
extract one or more of these 3 entities you need to add the key of the entities needed using the field custom_entities like this within your description:

```
"custom_entities": ["echo", "dir"]
```

:warning: If task is found, it will automatically add the field `TaskName` into the sidecar file. 
It means you don't have to add the field in the config file like this.

<strike>

```
{
     "sidecar_changes": {
        "TaskName": "learning"
    }
}
```

</strike>
   
:radioactive: You can find more detailed information by looking at the file `dcm2bids/utils/utils.py` and 
more specifically auto_extractors and auto_entities variables.


## --bids_validate

By default, Dcm2bids will not validate your final BIDS structure.
If needed, you can install [bids-validator](https://github.com/bids-standard/bids-validator#quickstart) and activate this option.
