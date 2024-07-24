# How to use main commands

## Command Line Interface (CLI) usage

See `dcm2bids -h` or `dcm2bids --help` to show the complete list of options and arguments.

```bash
--8<-- "docs_helper/help.txt"
```

### Main command: `dcm2bids`

```bash
dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -c CONFIG_FILE
```

If your participant have a session ID:

```bash
dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -s SESSION_ID -c CONFIG_FILE
```

!!! important

    If your directory or file names have space in them, we recommend that you
    change all the spaces for another character (`_` or `-`) but if you can't
    change the names, you have to wrap each argument with quotes as in the
    example below: 

    `dcm2bids -d "DICOM DIR" -p PARTICIPANT_ID -c "path/with spaces to/CONFIG FILE.json"`

## Output

dcm2bids creates a `sub-<PARTICIPANT_ID>` directory in the output directory (by
default the folder where the script is launched).

Sidecars with one matching description will be converted to BIDS. If a file
already exists, dcm2bids won't overwrite it. You should use the `--clobber`
option to overwrite files.

If a description matches several sidecars, dcm2bids will add automatically the
custom label `run-` to the filename.

Sidecars with no or more than one matching descriptions are kept in
`tmp_dcm2bids` directory. Users can review these mismatches to change the
configuration file accordingly.

dcm2bids creates log files inside `tmp_dcm2bids/log` directory.

## Tools

### Scaffold

the `dcm2bids_scaffold` command creates basic BIDS files and directories based on the [bids-starter-kit](https://github.com/bids-standard/bids-starter-kit). The output directory is set to the location where the script is launched by default.

```bash
dcm2bids_scaffold [-o OUTPUT_DIR]
```

```bash
--8<-- "docs_helper/help_scaffold.txt"
```

### Helper

To build the configuration file, you need to have examples of sidecar files. You
can use `dcm2bids_helper` with the DICOMs of one participant. It will launch
dcm2niix and save the result inside the `tmp_dcm2bids/helper` directory by default.

```bash
dcm2bids_helper -d DICOM_DIR [-o OUTPUT_DIR]
```

```bash
--8<-- "docs_helper/helper.txt"
```
[json-editor]: http://jsoneditoronline.org/

[^1]:
    For each acquisition, `dcm2niix` creates an associated `.json` file,
    containing information from the dicom header. These are known as
    **sidecars**. These are the sidecars `dcm2bids` uses to filter the groups of
    acquisitions.

    To define this filtering you will probably need to review these sidecars.
    You can generate all the sidecars for an individual participant using
    [dcm2bids_helper](./use-main-commands.md#tools).

--8<-- "docs_helper/abbreviations.md"
