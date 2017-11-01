# Dcm2Bids

Dcm2Bids helps you to reorganise the NIfTI files from [dcm2niix][dcm2niix-github] into the [Brain Imaging Data Structure][bids] (BIDS).

Before using this software, learn more about BIDS and read the [specifications][bids-spec].

## Install

```
git clone https://github.com/cbedetti/Dcm2Bids
```

Add the installation directory to your PYTHONPATH and the `scripts` directory to your PATH.

#### Dependencies

- Python 2 or 3. The `future` module should be installed. `pip install future`
- `dcm2niix` : DICOM to NIfTI conversion is done with `dcm2niix`. See [github][dcm2niix-github] for source code or [NITRC][dcm2niix-nitrc] for compiled versions.

## Usage

```
usage: dcm2bids [-h] -d DICOM_DIR [DICOM_DIR ...] -p PARTICIPANT [-s SESSION]
                -c CONFIG [-o OUTPUT_DIR] [--clobber] [--forceDcm2niix]
                [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

optional arguments:
  -h, --help            show this help message and exit
  -d DICOM_DIR [DICOM_DIR ...], --dicom_dir DICOM_DIR [DICOM_DIR ...]
                        DICOM files directory
  -p PARTICIPANT, --participant PARTICIPANT
                        Name of the participant
  -s SESSION, --session SESSION
                        Name of the session
  -c CONFIG, --config CONFIG
                        json configuration file
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Output BIDS directory, Default: current directory
  --clobber             Overwrite output if exists
  --forceDcm2niix       Overwrite old temporary dcm2niix output if exists
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}

example:
  dcm2bids -d sourcedata/s101/DICOM/ -s S101 -c code/config_dcm2bids.json
```

You need to build the configuration file of your study to let `dcm2bids` associate your acquisitions through BIDS sidecar. Every study is different and this step needs a little bit of work.

Sidecar files are `JSON` files with meta informations about the acquisition. These are created automatically with dcm2niix.

The dcm2bids configuration file uses also the `JSON` format and one example is provided in the `example` directory.

## Configuration file

```
{
    "descriptions": [
        {
            "dataType": "anat",
            "modalityLabel": "T2w",
            "criteria": {
                "SeriesDescription": "*T2*",
                "EchoTime": 0.1
            }
        },
        {
            "dataType": "func",
            "modalityLabel": "bold",
            "customLabels": "task-rest",
            "criteria": {
                "SidecarFilename": "006*"
            }
        }
    ]
}
```

The `descriptions` field is a list of description, each describing some acquisition. In this example, the configuration describes two acquisitions, a T2 weigthed and resting state fMRI.

#### `dataType`

It is a mandatory field. Here is a definition from `bids_specs1.0.2` pdf:

> A functional group of different types of MRI data. In BIDS we define four data types: func (task based and resting state functional MRI), dwi (diffusion weighted imaging), fmap (field inhomogeneity mapping data such as field maps), anat (structural imaging such as T1, T2, etc.)

#### `modalityLabel`

It is a mandatory field. It describes the modality of the acquisition like `T1w`, `T2w` or `bold`.

#### `customLabels`

It is an optional field. For some acquisitions, you need to add information in the file name. For resting state fMRI, it is usally `task-rest`.

To know more on how to set these fields, read the [BIDS specifications][bids-spec].

#### `criteria`

dcm2bids will try to match the sidecars of dcm2niix to the descriptions of the configuration file. The values you enter inside the criteria dictionnary are patterns. They will be compared to the corresponding key of the sidecar.

The pattern matching is shell-style. It's possible to use wildcard `*`, single character `?` etc ... Please have a look at the [GNU documentation][gnu-pattern] to know more.

For example, in the first description, the pattern `*T2*` will be compared to the value of `SeriesDescription` of a sidecar. `AXIAL_T2_SPACE` will be a match, `AXIAL_T1` won't.

`dcm2bids` create a `SidecarFilename` key if you prefer to also match with the filename of the sidecar.

You can enter several criteria. **All criteria must match** for a description to be link to a sidecar.

## Helper

`dcm2bids_helper -d DICOM_DIR`

To build the configuration file, you need to have a example of the sidecars. You can use `dcm2bids_helper` with the DICOMs of one participant. It will launch dcm2niix and save the result inside the `tmp_dcm2bids/dcm2niix-example` directory.

## Output

dcm2bids creates a `sub-<PARTICIPANT>` directory in the folder the script is launched.

Sidecars with one matching description will be convert to BIDS. If a file already exists, dcm2bids won't overwrite it. You should use the `--clobber` option to overwrite files.

If a description matches several sidecars, dcm2bids will add the custom label `run-` to the filename.

Sidecars with no or more than one matching descriptions are kept in `tmp_dcm2niix` directory. Users can review these mismatches to change the configuration file accordingly.


[bids]: http://bids.neuroimaging.io/
[bids-spec]: http://bids.neuroimaging.io/#download
[conda]: https://conda.io/docs/
[dcm2niix-github]: https://github.com/rordenlab/dcm2niix
[dcm2niix-nitrc]: https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage
[gnu-pattern]: https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html
