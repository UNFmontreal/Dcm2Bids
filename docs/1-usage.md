# Usage

## Introduction

dcm2bids converts one session at a time. A session is all the acquisitions between the entry and exit of the participant in the scanner.

You need to build a configuration file of your study to let dcm2bids associates your acquisitions through BIDS sidecar. Every study is different and this step needs a little bit of work. The scanner parameters should not change too much for one study (several MRI sessions), so a few configuration files should work.

BIDS sidecar[^1] files are `JSON` files with meta informations about the acquisition. `dcm2niix` (DICOM to NIfTI converter used by dcm2bids) creates automatically one BIDS sidecar for each NIfTI file.

dcm2bids configuration file uses also the `JSON` format. One example is provided in the `example` folder on the github repository.

It is recommended to use an editor with syntax highlighting to build a correct JSON file. Here is an [online][json-editor] one.

## Command Line Interface (CLI)

How to launch dcm2bids when you have build your configuration file ? First `cd` in your BIDS directory.

```bash
dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -c CONFIG_FILE
```

If your participant have a session ID:

```bash
dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -s SESSION_ID -c CONFIG_FILE
```

dcm2bids creates log files inside `tmp_dcm2bids/log`

See `dcm2bids -h` or `dcm2bids --help` to show the help message that contains more information.

## Output

dcm2bids creates a `sub-<PARTICIPANT_ID>` directory in the output directory (by default the folder where the script is launched).

Sidecars with one matching description will be convert to BIDS. If a file already exists, dcm2bids won't overwrite it. You should use the `--clobber` option to overwrite files.

If a description matches several sidecars, dcm2bids will add automatically the custom label `run-` to the filename.

Sidecars with no or more than one matching descriptions are kept in `tmp_dcm2bids` directory. Users can review these mismatches to change the configuration file accordingly.

## Tools

- Helper

```bash
dcm2bids_helper -d DICOM_DIR [-o OUTPUT_DIR]
```

To build the configuration file, you need to have a example of the sidecars. You can use `dcm2bids_helper` with the DICOMs of one participant. It will launch dcm2niix and save the result inside the `tmp_dcm2bids/helper` of the output directory.

- Scaffold

```bash
dcm2bids_scaffold [-o OUTPUT_DIR]
```

Create basic BIDS files and directories in the output directory (by default folder where the script is launched).

[json-editor]: http://jsoneditoronline.org/


# Containers

You can also use all the tools through docker or singularity images.

=== "Docker"
    ```console
    docker pull unfmontreal/dcm2bids:latest
    ```

=== "Singularity"
    ```console
    singularity pull dcm2bids_latest.sif docker://unfmontreal/dcm2bids:latest
    ```
   
[^1]: For each acquisition, `dcm2niix` creates an associated `.json` file,
    containing information from the dicom header. These are known as
    __sidecars__. These are the sidecars `dcm2bids` uses to filter the groups
    of acquisitions.

    To define this filtering you will probably need to review these sidecars.
    You can generate all the sidecars for an individual participant using [dcm2bids_helper](1-usage.md#tools).
