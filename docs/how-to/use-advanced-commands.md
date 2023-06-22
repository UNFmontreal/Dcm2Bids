# How to use advanced configuration

These optional configurations could be insert in the configuration file at the
same level as the `"descriptions"` entry.

```
{
    "extractors": {"SeriesDescription": ["run-(?P<run>[0-9]+)", "task-(?P<task>[0-9]+)"], 
                   "BodyPartExamined": ["(?P<bodypart>[a-zA-Z]+)"]},
    "searchMethod": "fnmatch",
    "caseSensitive": true,
    "defaceTpl": ["pydeface", "--outfile", "dstFile", "srcFile"],
    "description": [
    {
      "dataType": "anat",
      "modalityLabel": "T2w",
      "customEntities": ["acq-highres", "bodypart", "run", "task"],
      }
    ]
    ...
}
```

## customEntities combined with extractors

default: None

extractors will allow you to extract information embeded into sidecar files. 
In the example above, it will try to match 2 different regex expressions (keys: task, run) within the 
SeriesDescription field and bodypart in BodyPartExamined field.

By using the same keys in customEntities and if found, it will add this new entities directly into the final filename.
customEntities can be a list that combined extractor keys and regular entities. 
If key is `task` it will automatically add the field "TaskName" inside the sidecase file.

## searchMethod

default: `"searchMethod": "fnmatch"`

fnmatch is the behaviour (See criteria) by default and the fall back if this
option is set incorrectly. `re` is the other choice if you want more flexibility
to match criteria.

## caseSensitive

default: `"caseSensitive": "true"`

If false, comparisons between strings/lists will be not case sensitive. It's
only disabled when used with `"searchMethod": "fnmatch"`.

## defaceTpl

default: `"defaceTpl": None`

!!! danger The anonymizer option no longer exists from `v2.0.0`. It is still
possible to deface the anatomical nifti images.

For example, if you use the last version of pydeface, add:

`"defaceTpl": "pydeface --outfile {dstFile} {srcFile}"`

It is a template string and dcm2bids will replace {srcFile} and {dstFile} by the
source file (input) and the destination file (output).

## dcm2niixOptions

default: `"dcm2niixOptions": "-b y -ba y -z y -f '%3s_%f_%p_%t'"`

Arguments for dcm2niix

## compKeys

default: `"compKeys": ["SeriesNumber", "AcquisitionTime", "SidecarFilename"]`

Acquisitions are sorted using the sidecar data. The default behaviour is to sort
by `SeriesNumber` then by `AcquisitionTime` then by the `SidecarFilename`. You
can change this behaviour setting this key inside the configuration file.


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
    usage: dcm2bids [-h] -d DICOM_DIR [DICOM_DIR ...] -p PARTICIPANT [-s SESSION] -c CONFIG [-o OUTPUT_DIR] [--forceDcm2niix] [--clobber]
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
                            depending on the suffix and dataType. [False]
    --bids_validate       If set, once your conversion is done it will check if your output folder is BIDS valid. [False]
                          bids-validator needs to be installed check: https://github.com/bids-standard/bids-validator#quickstart
    --forceDcm2niix       Overwrite previous temporary dcm2niix output if it exists
    --clobber             Overwrite output if it exists
    -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                            Set logging level
    -a, --anonymizer      This option no longer exists from the script in this release. See:https://github.com/unfmontreal/Dcm2Bids/blob/master/README.md#defaceTpl

                Documentation at https://github.com/unfmontreal/Dcm2Bids

    ```

## --auto_extract_entities

This option will automatically try to find 3 entities (task, dir and echo) for specific dataType/modalityLabel.

* `task` in the SeriesDescription field

    Regex expression `task-(?P<task>[a-zA-Z0-9]+)`

* `dir` in the PhaseEncodedDirection field

    Regex expression `(?P<dir>-?j|i)`

* `echo` in the EchoNumber field 

    Regex expression `(?P<echo>[0-9])`

If found, it will try to feed the filename with this entity if they are mandatory.

For example, a "pepolar" fieldmap data requires the entity `dir` (See [BIDS specification](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#case-4-multiple-phase-encoded-directions-pepolar)). 
If you set this parameter, it will automatically try to find this entity and add it to the filename.

So far and accordingly to the BIDS specification 5 dataType/modalityLabel automatically look for this 3 entities.

| dataType |  modalityLabel | Entities |
|:--------:|:----------:|:--------:|
| anat | MEGRE | echo |
| anat | MESE | echo |
| func | cbv | task |
| func | bold | task |
| func | sbref | task |
| fmap | epi | dir |

Using the `--auto_extract_entitie`, if you want another combination of dataType/modalityLabel to be able to 
extract one or more of these 3 entities you need to add the key of the entities needed using the field customEntities like this within your description:

```
"customEntities": ["echo", "dir"]
```

:warning: If task is found, it will automatically add the field `TaskName` into the sidecar file. 
It means you don't have to add the field in the config file like this.

<strike>

```
{
     "sidecarChanges": {
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
