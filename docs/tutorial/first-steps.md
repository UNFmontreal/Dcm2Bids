# Tutorial - First steps

## How to use this tutorial

This tutorial was developed assuming no prior knowledge of the tool, and little
knowledge of the command line (terminal). It aims to be beginner-friendly by
giving a lot of details. To get the most out of it, you recommend that you run
the commands throughout the tutorial and compare your outputs with the outputs
from the example.

Every time you need to run a command, you will see two tabs, one for the command
you need to run, and another one with the expected output. While you can copy
the command, you recommend that you type each command, which is good for your
procedural memory :brain:. The **Command** and **Output** tabs will look like
these:

=== "Command"

    ```sh
    echo "Hello, World!"
    ```

=== "Output"

    ```sh
    sam:~/$ echo "Hello, World!"
    Hello, World!
    ```

Note that in the Output tab, the content before the command prompt (`$`) will be
dependend or your operating system and terminal configuration. What you want to
compare is what follows it and the output below the command that was ran. The
output you see was taken directly out of your terminal when you tested the
tutorial.

## Setup

!!! warning "dcm2bids must be installed"

    If you have not installed dcm2bids yet, now is the time to go to the [installation page](../get-started/install.md) and install dcm2bids with its dependencies. This tutorial does not cover the installation part and assumes you have dcm2bids properly installed.

### Activate your dcm2bids environment

If you followed the [installation procedure](../get-started/install.md), you
have to activate your dedicated environment for dcm2bids.

Note that you use `dcm2bids` as the name of the environment but you should use
the name you gave your environment when you created it.

If you used Anaconda Navigator to install dcm2bids and create you environment,
make sure to open your environment from Navigator as indicated in [Create your environment with the Anaconda Navigator GUI](../get-started/install.md#install-dcm2bids).

=== "Command"

    ```sh
    conda activate dcm2bids
    ```

=== "Output"

    ```sh
    conda activate dcm2bids
    (dcm2bids) sam:~$
    ```

### Test your environment

It is always good to make sure you have access to the software you want to use.
You can test it with any command but a safe way is to use the `--help` command.

=== "Command"

    ```sh
    dcm2bids --help
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~$ dcm2bids --help
    usage: dcm2bids [-h] -d DICOM_DIR [DICOM_DIR ...] -p PARTICIPANT [-s SESSION] -c
                    CONFIG [-o OUTPUT_DIR] [--forceDcm2niix] [--clobber]
                    [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-a]

    Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure
    dcm2bids 2.1.7

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
                            Output BIDS directory, Default: current directory
                            (/home/sam)
    --forceDcm2niix       Overwrite previous temporary dcm2niix output if it exists
    --clobber             Overwrite output if it exists
    -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                            Set logging level
    -a, --anonymizer      This option no longer exists from the script in this
                            release. See:https://github.com/unfmontreal/Dcm2Bids/blob/m
                            aster/README.md#defaceTpl

                Documentation at https://github.com/unfmontreal/Dcm2Bids

    ```

??? bug "What you can do if you did not get this output"

    If you got `dcm2bids: command not found`, it means dcm2bids is not either not installed or not accessible in your current environment. Did you activate your environment?

    Visit the [installation page](../get-started/install.md) for more info.

### Create a new directory for this tutorial

For the tutorial, you recommend that you create a new directory (folder) instead
of jumping straight into a real project directory with real data. In this
tutorial, we decided to named our project directory `dcm2bids-tutorial`.

=== "Command"

    ```sh
    mkdir dcm2bids-tutorial
    cd dcm2bids-tutorial
    ```

=== "Output"

    ```bash
    (dcm2bids) sam:~$ mkdir dcm2bids-tutorial
    (dcm2bids) sam:~$ cd dcm2bids-tutorial/
    (dcm2bids) sam:~/dcm2bids-tutorial$
    # no output is printed by mkdir and cd if when the command is successful.
    # You can now see that you are inside dcm2bids-tutorial directory.
    ```

## Scaffolding

While scaffolding is a not mandatory step before converting data with the main
`dcm2bids` command, it is highly recommended when you plan to convert data.
dcm2bids has a command named **`dcm2bids_scaffold`** that will help you
structure and organize your data in an efficient way by creating automatically
for you a basic directory structure and the core files according to the [Brain
Imaging Data Structure (BIDS) specification][bids-spec].

### Tree structure of the scaffold created by dcm2bids

```sh
scaffold_directory/
├── CHANGES
├── code/
├── dataset_description.json
├── derivatives/
├── participants.json
├── participants.tsv
├── README
└── sourcedata/

3 directories, 5 files
```

Describing the function of each directory and files is out of the scope of this
tutorial but if you want to learn more about BIDS, you encourage you to go
through the [BIDS Starter Kit][bids-starter-kit].

### Run `dcm2bids_scaffold`

To find out how to run `dcm2bids_scaffold` work, you can use the `--help`
option.

=== "Command"

    ```sh
    dcm2bids_scaffold --help
    ```

=== "Output"

    ```sh hl_lines="9-10"
    (dcm2bids) sam:~/dcm2bids-tutorial$ dcm2bids_scaffold --help
    usage: dcm2bids_scaffold [-h] [-o OUTPUT_DIR]

                Create basic BIDS files and directories


    options:
    -h, --help            show this help message and exit
    -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            Output BIDS directory, Default: current directory

                Documentation at https://github.com/unfmontreal/Dcm2Bids

    ```

As you can see at lines 9-10, `dcm2bids_scaffold` has an `--output_dir` (or `-o`
for short) option with a default option, which means you can either specify
where you want the scaffolding to happen to be or it will create the scaffold in
the current directory as a default.

Below you can see the difference between specifying `-o output_dir` and NOT
specifying (using the default) the `-o` option.

Note that you don't have to create the directory where you want to put the
scaffold beforehand, the command will create it for you.

=== "Commands"

    ```sh
    dcm2bids_scaffold
    ```
    **VS**

    ```sh
    dcm2bids_scaffold -o bids_project
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial$ dcm2bids_scaffold
    (dcm2bids) sam:~/dcm2bids-tutorial$ ls
    CHANGES  dataset_description.json  participants.json  README
    code     derivatives               participants.tsv   sourcedata

    ```
    **VS**

    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial$ dcm2bids_scaffold -o bids_project
    (dcm2bids) sam:~/dcm2bids-tutorial$ ls -F
    bids_project/
    (dcm2bids) sam:~/dcm2bids-tutorial$ ls -F bids_project/
    CHANGES  dataset_description.json  participants.json  README
    code/    derivatives/              participants.tsv   sourcedata/
    ```

For the purpose of the tutorial, you chose to specify the output directory
**`bids_project`** as if it were the start of a new project. For your real
projects, you can choose to create a new directory with the commands or not, it
is entirely up to you.

### Change directory to go in your scaffold

For those who created the scaffold in another directory, you must go inside that
directory.

=== "Command"

    ```sh
    cd bids_project
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial$ cd bids_project/
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$
    ```

## Download neuroimaging data

For this tutorial, you will use a set of DICOMs made available by
[neurolabusc][dcm_qa_nih] on GitHub.

??? info "Why use these data in particular?"

    You use the [dcm_qa_nih][dcm_qc_nih] data because it is the data used by the
    dcm2niix developers to validate the DICOM to NIfTI conversion process and it
    has been proven stable since 2017. It also includes data from both GE as
    well as Siemens MRI scanners so it gives a bit a diversity of data provenance.

To download the data, you can use your terminal or the GitHub interface. You can
do it any way you want as long as the directory with the dicoms is in
**sourcedata** directory with the name **dcm_qa_nih**.

=== "Terminal"

    === "Commands"

        1. Download the zipped file from <https://github.com/neurolabusc/dcm_qa_nih/archive/refs/heads/master.zip>.
        ```sh
        wget -O dcm_qa_nih-master.zip https://github.com/neurolabusc/dcm_qa_nih/archive/refs/heads/master.zip
        ```

        2. Extract/unzip the zipped file into **sourcedata/**.
        ```sh
        unzip dcm_qa_nih-master.zip -d sourcedata/
        ```

        3. Rename the directory **dcm_qa_nih**.
        ```sh
        mv sourcedata/dcm_qa_nih-master sourcedata/dcm_qa_nih
        ```

        **OR**

        1. You can clone the repository if you are familiar with Git. If you did the
        steps above, move on.
        ```sh
        git clone https://github.com/neurolabusc/dcm_qa_nih/ sourcedata/dcm_qa_nih
        ```

        ---

    === "Output"

        ```sh hl_lines="1 18 33"
        (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ wget -O dcm_qa_nih-master.zip https://github.com/neurolabusc/dcm_qa_nih/archive/refs/heads/master.zip
        --2022-04-18 22:17:26--  https://github.com/neurolabusc/dcm_qa_nih/archive/refs/heads/master.zip
        Resolving github.com (github.com)... 140.82.112.3
        Connecting to github.com (github.com)|140.82.112.3|:443... connected.
        HTTP request sent, awaiting response... 302 Found
        Location: https://codeload.github.com/neurolabusc/dcm_qa_nih/zip/refs/heads/master [following]
        --2022-04-18 22:17:26--  https://codeload.github.com/neurolabusc/dcm_qa_nih/zip/refs/heads/master
        Resolving codeload.github.com (codeload.github.com)... 140.82.113.9
        Connecting to codeload.github.com (codeload.github.com)|140.82.113.9|:443... connected.
        HTTP request sent, awaiting response... 200 OK
        Length: 10258820 (9.8M) [application/zip]
        Saving to: ‘dcm_qa_nih-master.zip’

        dcm_qa_nih-master.zip 100%[======================>]   9.78M  3.24MB/s    in 3.0s

        2022-04-18 22:17:29 (3.24 MB/s) - ‘dcm_qa_nih-master.zip’ saved [10258820/10258820]

        (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ unzip dcm_qa_nih-master.zip -d sourcedata/
        Archive:  dcm_qa_nih-master.zip
        aa82e560d5471b53f0d0332c4de33d88bf179157
        creating: sourcedata/dcm_qa_nih-master/
        extracting: sourcedata/dcm_qa_nih-master/.gitignore
        creating: sourcedata/dcm_qa_nih-master/In/
        creating: sourcedata/dcm_qa_nih-master/In/20180918GE/
        inflating: sourcedata/dcm_qa_nih-master/In/20180918GE/README-Study.txt
        creating: sourcedata/dcm_qa_nih-master/In/20180918GE/mr_0004/
        inflating: sourcedata/dcm_qa_nih-master/In/20180918GE/mr_0004/README-Series.txt
        inflating: sourcedata/dcm_qa_nih-master/In/20180918GE/mr_0004/axial_epi_fmri_interleaved_i_to_s-00001.dcm
        # [...] output was manually truncated because it was really really long
        inflating: sourcedata/dcm_qa_nih-master/Ref/EPI_PE=RL_5.nii
        inflating: sourcedata/dcm_qa_nih-master/batch.sh
        (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ mv sourcedata/dcm_qa_nih-master sourcedata/dcm_qa_nih
        ```

        ---

=== "GitHub"

    1. Go to: [https://github.com/neurolabusc/dcm_qa_nih][dcm_qc_nih] and click on the
    green button (Code) to **download ZIP**.

    ![](../assets/img/dcm_qa_nih_repo-dark.png#border#only-dark){ loading=lazy }
    ![](../assets/img/dcm_qa_nih_repo-light.png#border#only-light){ loading=lazy }

    1. Download the zipped file.
    2. Extract/unzip the zipped file to the **sourcedata** directory inside
    your scaffold and rename the newly created directory **dcm_qa_nih**.

    ---

You should now have a `dcm_qa_nih` directory nested in `sourcedata` with a bunch
of files and directories:

=== "Command"

    ```sh
    ls sourcedata/dcm_qa_nih
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ ls sourcedata/dcm_qa_nih/
    batch.sh  In  LICENSE  README.md  Ref
    ```

## Building the configuration file

The configuration file is the central element for dcm2bids to organize your data
into the [Brain Imaging Data Structure][bids-spec] standard. dcm2bids uses
information from the config file to determine which data in the protocol will be
converted, and how they will be renamed based on a set of rules. For this
reason, it is important to have a little understanding of the core BIDS
principles. The [BIDS Starter Kit][bids-starter-kit] a good place to start
[Tutorial on Annotating a BIDS dataset][bids-starter-kit-annot] from .

As you will see below, the configuration file must be structured in the
Javascript Object Notation (JSON) format.

!!! info "More info about the configuration file"

    The [How-to guide on creating a config file][config] provides useful
    information about required and optional fields, and the inner working of a
    config file.

In short you need a configuration file because, for each acquisition, `dcm2niix`
creates an associated `.json` file, containing information from the dicom
header. These are known as **sidecar files**. These are the sidecars that
`dcm2bids` uses to filter the groups of acquisitions based on the configuration
file.

You have to input the filters yourself, which is way easier to define when you
have access to an example of the sidecar files.

You can generate all the sidecar files for an individual participant using the
[dcm2bids_helper](./use-main-commands.md#tools) command.

### `dcm2bids_helper` command

This command will convert the DICOM files it finds to NIfTI files and save them
inside a temporary directory for you to inspect and make some filters for the
config file.

As usual the first command will be to request the help info.

=== "Command"

    ```sh
    dcm2bids_helper --help
    ```

=== "Output"

    ```sh hl_lines="6 8"
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ dcm2bids_helper --help
    usage: dcm2bids_helper [-h] -d DICOM_DIR [DICOM_DIR ...] [-o OUTPUT_DIR]

    options:
    -h, --help            show this help message and exit
    -d DICOM_DIR [DICOM_DIR ...], --dicom_dir DICOM_DIR [DICOM_DIR ...]
                            DICOM files directory
    -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                            Output BIDS directory, Default: current directory

                Documentation at https://github.com/unfmontreal/Dcm2Bids
    ```

To run the commands, you have to specify the `-d` option, namely the input
directory containing the DICOM files. The `-o` option is optional, defaulting to
moving the files inside a new `tmp_dcm2bids/helper` directory from where you run
the command, the current directory.

!!! tip "Use one participant only"

    For this tutorial, it is easy since you there are only few data. However, in
    project with many participants, it is recommended to use data from one
    one session of one participant only by targeting their directory, otherwise you may be overwhelmed
    by the number of files for nothing.

    In this tutorial, there are two folders with data, one with data coming from a
    Siemens scanner (`20180918Si`), and one with data coming from GE (20180918GE).
    The tutorial will use the data acquired on both scanners and Siemens scanner
    located in `sourcedata/dcm_qa_nih/In/` and pretend it is one participant only.

=== "Command"

    ```sh
    dcm2bids_helper -d sourcedata/dcm_qa_nih/In/
    ```

=== "Output"

    ```sh hl_lines="4"
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ dcm2bids_helper -d sourcedata/dcm_qa_nih/In/
    Example in:
    /home/sam/dcm2bids-tutorial/bids_project/tmp_dcm2bids/helper
    ```

### Finding what you need in **tmp_dcm2bids/helper**

You should now able to see a list of compressed NIfTI files (`nii.gz`) with
their respective sidecar files (`.json`). You can tell which file goes with
which file based on their identical names, only with a

=== "Command"

    ```sh
    ls tmp_dcm2bids/helper
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ ls tmp_dcm2bids/helper/
    '003_In_EPI_PE=AP_20180918121230.json'
    '003_In_EPI_PE=AP_20180918121230.nii.gz'
    004_In_DCM2NIIX_regression_test_20180918114023.json
    004_In_DCM2NIIX_regression_test_20180918114023.nii.gz
    '004_In_EPI_PE=PA_20180918121230.json'
    '004_In_EPI_PE=PA_20180918121230.nii.gz'
    005_In_DCM2NIIX_regression_test_20180918114023.json
    005_In_DCM2NIIX_regression_test_20180918114023.nii.gz
    '005_In_EPI_PE=RL_20180918121230.json'
    '005_In_EPI_PE=RL_20180918121230.nii.gz'
    006_In_DCM2NIIX_regression_test_20180918114023.json
    006_In_DCM2NIIX_regression_test_20180918114023.nii.gz
    '006_In_EPI_PE=LR_20180918121230.json'
    '006_In_EPI_PE=LR_20180918121230.nii.gz'
    007_In_DCM2NIIX_regression_test_20180918114023.json
    007_In_DCM2NIIX_regression_test_20180918114023.nii.gz
    ```

As you can see, it is not necessarily easy to tell which scan files (`nii.gz`)
refer to which acquisitions from their names only. That is why you have to go
through their sidecar files to find unique identifiers for one acquisiton you
want to _BIDSify_.

Go ahead and use any code editor, file viewer or your terminal to inspect the
sidecar files.

Here, we compare two files that have similar names to highlight their
differences:

=== "Command"

    ```sh
    diff --side-by-side tmp_dcm2bids/helper/"003_In_EPI_PE=AP_20180918121230.json" tmp_dcm2bids/helper/"004_In_EPI_PE=PA_20180918121230.json"
    ```

    - Note than in this example, the filename are wrapped with quotes (`"`) as in
    `"filename.ext"` because there is an `=` include in the name. You have to wrap
    your filenames if they contains special characters, including spaces. To avoid
    weird problems, we highly recommend to use alphanumeric only names when you
    can choose the name of your MRI protocols and sequences.

=== "Output"

    ```sh hl_lines="18 19 25 26 66 69 71 72"
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ diff --side-by-side tmp_dcm2bids/helper/003_In_EPI_PE\=AP_20180918121230.json tmp_dcm2bids/helper/004_In_EPI_PE\=PA_20180918121230.json
    {                                                           {
        "Modality": "MR",                                           "Modality": "MR",
        "MagneticFieldStrength": 3,                                 "MagneticFieldStrength": 3,
        "ImagingFrequency": 123.204,                                "ImagingFrequency": 123.204,
        "Manufacturer": "Siemens",                                  "Manufacturer": "Siemens",
        "ManufacturersModelName": "Skyra",                          "ManufacturersModelName": "Skyra",
        "InstitutionName": "NIH",                                   "InstitutionName": "NIH",
        "InstitutionalDepartmentName": "FMRIF 3TD",                 "InstitutionalDepartmentName": "FMRIF 3TD",
        "InstitutionAddress": "10 Center Drive Building 10 Ro       "InstitutionAddress": "10 Center Drive Building 10 Ro
        "DeviceSerialNumber": "45160",                              "DeviceSerialNumber": "45160",
        "StationName": "AWP45160",                                  "StationName": "AWP45160",
        "BodyPartExamined": "BRAIN",                                "BodyPartExamined": "BRAIN",
        "PatientPosition": "HFS",                                   "PatientPosition": "HFS",
        "ProcedureStepDescription": "FMRIF^QA",                     "ProcedureStepDescription": "FMRIF^QA",
        "SoftwareVersions": "syngo MR E11",                         "SoftwareVersions": "syngo MR E11",
        "MRAcquisitionType": "2D",                                  "MRAcquisitionType": "2D",
        "SeriesDescription": "EPI PE=AP",                      |    "SeriesDescription": "EPI PE=PA",
        "ProtocolName": "EPI PE=AP",                           |    "ProtocolName": "EPI PE=PA",
        "ScanningSequence": "EP",                                   "ScanningSequence": "EP",
        "SequenceVariant": "SK",                                    "SequenceVariant": "SK",
        "ScanOptions": "FS",                                        "ScanOptions": "FS",
        "SequenceName": "epfid2d1_72",                              "SequenceName": "epfid2d1_72",
        "ImageType": ["ORIGINAL", "PRIMARY", "M", "ND", "ECHO       "ImageType": ["ORIGINAL", "PRIMARY", "M", "ND", "ECHO
        "SeriesNumber": 3,                                     |    "SeriesNumber": 4,
        "AcquisitionTime": "12:24:58.102500",                  |    "AcquisitionTime": "12:26:54.517500",
        "AcquisitionNumber": 1,                                     "AcquisitionNumber": 1,
        "ImageComments": "None",                                    "ImageComments": "None",
        "SliceThickness": 3,                                        "SliceThickness": 3,
        "SpacingBetweenSlices": 12,                                 "SpacingBetweenSlices": 12,
        "SAR": 0.00556578,                                          "SAR": 0.00556578,
        "EchoTime": 0.05,                                           "EchoTime": 0.05,
        "RepetitionTime": 2.43537,                                  "RepetitionTime": 2.43537,
        "FlipAngle": 75,                                            "FlipAngle": 75,
        "PartialFourier": 1,                                        "PartialFourier": 1,
        "BaseResolution": 72,                                       "BaseResolution": 72,
        "ShimSetting": [                                            "ShimSetting": [
            -3717,                                                      -3717,
            15233,                                                      15233,
            -9833,                                                      -9833,
            -207,                                                       -207,
            -312,                                                       -312,
            -110,                                                       -110,
            150,                                                        150,
            226    ],                                                   226],
        "TxRefAmp": 316.97,                                         "TxRefAmp": 316.97,
        "PhaseResolution": 1,                                       "PhaseResolution": 1,
        "ReceiveCoilName": "Head_32",                               "ReceiveCoilName": "Head_32",
        "ReceiveCoilActiveElements": "HEA;HEP",                     "ReceiveCoilActiveElements": "HEA;HEP",
        "PulseSequenceDetails": "%CustomerSeq%\\nih_ep2d_bold       "PulseSequenceDetails": "%CustomerSeq%\\nih_ep2d_bold
        "CoilCombinationMethod": "Sum of Squares",                  "CoilCombinationMethod": "Sum of Squares",
        "ConsistencyInfo": "N4_VE11C_LATEST_20160120",              "ConsistencyInfo": "N4_VE11C_LATEST_20160120",
        "MatrixCoilMode": "SENSE",                                  "MatrixCoilMode": "SENSE",
        "PercentPhaseFOV": 100,                                     "PercentPhaseFOV": 100,
        "PercentSampling": 100,                                     "PercentSampling": 100,
        "EchoTrainLength": 72,                                      "EchoTrainLength": 72,
        "PhaseEncodingSteps": 72,                                   "PhaseEncodingSteps": 72,
        "AcquisitionMatrixPE": 72,                                  "AcquisitionMatrixPE": 72,
        "ReconMatrixPE": 72,                                        "ReconMatrixPE": 72,
        "BandwidthPerPixelPhaseEncode": 27.778,                     "BandwidthPerPixelPhaseEncode": 27.778,
        "EffectiveEchoSpacing": 0.000499996,                        "EffectiveEchoSpacing": 0.000499996,
        "DerivedVendorReportedEchoSpacing": 0.000499996,            "DerivedVendorReportedEchoSpacing": 0.000499996,
        "TotalReadoutTime": 0.0354997,                              "TotalReadoutTime": 0.0354997,
        "PixelBandwidth": 2315,                                     "PixelBandwidth": 2315,
        "DwellTime": 3e-06,                                         "DwellTime": 3e-06,
        "PhaseEncodingDirection": "j-",                        |    "PhaseEncodingDirection": "j",
        "SliceTiming": [                                            "SliceTiming": [
            0,                                                          0,
            1.45,                                              |        1.4475,
            0.4825,                                                     0.4825,
            1.9325,                                            |        1.93,
            0.9675    ],                                       |        0.965    ],
        "ImageOrientationPatientDICOM": [                           "ImageOrientationPatientDICOM": [
            1,                                                          1,
            0,                                                          0,
            0,                                                          0,
            0,                                                          0,
            1,                                                          1,
            0    ],                                                     0   ],
        "ImageOrientationText": "Tra",                              "ImageOrientationText": "Tra",
        "InPlanePhaseEncodingDirectionDICOM": "COL",                "InPlanePhaseEncodingDirectionDICOM": "COL",
        "ConversionSoftware": "dcm2niix",                           "ConversionSoftware": "dcm2niix",
        "ConversionSoftwareVersion": "v1.0.20211006"                "ConversionSoftwareVersion": "v1.0.20211006"
    }                                                           }

    ```

Again, when you will do it with your DICOMs, you will want to run
`dcm2bids_helper` on a typical session of one of your participants. You will
probably get more files than this example

For the purpose of the tutorial, we will be interested in three specific
acquisitions, namely:

1. `004_In_DCM2NIIX_regression_test_20180918114023`
2. `003_In_EPI_PE=AP_20180918121230`
3. `004_In_EPI_PE=PA_20180918121230`

The first is an resting-state fMRI acquisiton whereas the second and third are
fieldmap EPI.

### Setting up the configuration file

Once you found the data you want to _BIDSify_, you can start setting up your
configuration file. The file name is arbritrary but for the readibility purpose,
you can name it `dcm2bids_config.json` like in the tutorial. You can create in
the `code/` directory. Use any code editor to create the file and add the
following content:

```json
{
  "descriptions": []
}
```

=== "Command"

    ```sh
    nano code/dcm2bids_config.json
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ nano code/dcm2bids_config.json
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$
    # No output is shown since nano is an interactive terminal-based editor
    ```

#### Populating the config file

To populate the config file, you need to inspect each sidecar files one at a
time and make sure there is a unique match for the acquisition you target. For
example, with the resting-state fMRI data
(`004_In_DCM2NIIX_regression_test_20180918114023`). You can inspect its sidecar
file and look for the `"SeriesDescription"` field for example. It is often a
good unique identifier.

=== "Command"

    ```sh
    cat code/dcm2bids_config.json
    ```

=== "Output"

    ```sh hl_lines="17"
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ cat tmp_dcm2bids/helper/004_In_DCM2NIIX_regression_test_20180918114023.json
    {
        "Modality": "MR",
        "MagneticFieldStrength": 3,
        "ImagingFrequency": 127.697,
        "Manufacturer": "GE",
        "PulseSequenceName": "epiRT",
        "InternalPulseSequenceName": "EPI",
        "ManufacturersModelName": "DISCOVERY MR750",
        "InstitutionName": "NIH FMRIF",
        "DeviceSerialNumber": "000301496MR3T6MR",
        "StationName": "fmrif3tb",
        "BodyPartExamined": "BRAIN",
        "PatientPosition": "HFS",
        "SoftwareVersions": "27\\LX\\MR Software release:DV26.0_R01_1725.a",
        "MRAcquisitionType": "2D",
        "SeriesDescription": "Axial EPI-FMRI (Interleaved I to S)",
        "ProtocolName": "DCM2NIIX regression test",
        "ScanningSequence": "EP\\GR",
        "SequenceVariant": "SS",
        "ScanOptions": "EPI_GEMS\\PFF",
        "ImageType": ["ORIGINAL", "PRIMARY", "EPI", "NONE"],
        "SeriesNumber": 4,
        "AcquisitionTime": "11:48:15.000000",
        "AcquisitionNumber": 1,
        "SliceThickness": 3,
        "SpacingBetweenSlices": 5,
        "SAR": 0.0166392,
        "EchoTime": 0.03,
        "RepetitionTime": 5,
        "FlipAngle": 60,
        "PhaseEncodingPolarityGE": "Unflipped",
        "CoilString": "32Ch Head",
        "PercentPhaseFOV": 100,
        "PercentSampling": 100,
        "AcquisitionMatrixPE": 64,
        "ReconMatrixPE": 64,
        "EffectiveEchoSpacing": 0.000388,
        "TotalReadoutTime": 0.024444,
        "PixelBandwidth": 7812.5,
        "PhaseEncodingDirection": "j-",
        "SliceTiming": [
            0,
            2.66667,
            0.333333,
            3,
            0.666667,
            3.33333,
            1,
            3.66667,
            1.33333,
            4,
            1.66667,
            4.33333,
            2,
            4.66667,
            2.33333	],
        "ImageOrientationPatientDICOM": [
            1,
            -0,
            0,
            -0,
            1,
            0	],
        "InPlanePhaseEncodingDirectionDICOM": "COL",
        "ConversionSoftware": "dcm2niix",
        "ConversionSoftwareVersion": "v1.0.20211006"
    }
    ```

To match the `"SeriesDescription"` field, a pattern like `Axial EPI-FMRI*` could
match it. However, we need to make sure we will match only one acquisition. You
can test it by looking manually at inside all sidecar files but it is now
recommend. It is rather trivial for the computer to look in all the .json files
for you with the `grep` command:

=== "Command"

    ```sh
    grep "Axial EPI-FMRI*" tmp_dcm2bids/helper/*.json
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ grep "Axial EPI-FMRI*" tmp_dcm2bids/helper/*.json
    tmp_dcm2bids/helper/004_In_DCM2NIIX_regression_test_20180918114023.json:	"SeriesDescription": "Axial EPI-FMRI (Interleaved I to S)",
    tmp_dcm2bids/helper/005_In_DCM2NIIX_regression_test_20180918114023.json:	"SeriesDescription": "Axial EPI-FMRI (Sequential I to S)",
    tmp_dcm2bids/helper/006_In_DCM2NIIX_regression_test_20180918114023.json:	"SeriesDescription": "Axial EPI-FMRI (Interleaved S to I)",
    tmp_dcm2bids/helper/007_In_DCM2NIIX_regression_test_20180918114023.json:	"SeriesDescription": "Axial EPI-FMRI (Sequential S to I)",
    ```

Unfortunately, this criteria is not enough and it could match other 4 files.

In this situation, you can add another criteria to match the specific
acquisition. Which one do you think would be more appropriate? Go back to the
content of the fMRI sidecar file and find a another criteria that, in
combination with the `"SeriesDescription"`, will uniquely match the fMRI data.

Right, maybe instead of trying to look for another field, you could simply
extend the criteria for the `"SeriesDescription"`. How many files does it match
if you extend it to the full value (`Axial EPI-FMRI (Interleaved I to S)`?

=== "Command"

    ```sh
    grep "Axial EPI-FMRI (Interleaved I to S)*" tmp_dcm2bids/helper/*.json
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ grep "Axial EPI-FMRI (Interleaved I to S)*" tmp_dcm2bids/helper/*.json
    tmp_dcm2bids/helper/004_In_DCM2NIIX_regression_test_20180918114023.json:	"SeriesDescription": "Axial EPI-FMRI (Interleaved I to S)",
    ```

:tada:, there is only one match! It means you can now update your configuration
file by adding a couple of necessary fields for which you can find a description
in [How to create a config file][config]. Since it is a resting-stage fMRI
acquisition, you want to specify it like this then make dcm2bids change your
task name:

```json hl_lines="3-10"
{
  "descriptions": [
    {
      "dataType": "func",
      "modalityLabel": "bold",
      "customLabels": "task-rest",
      "criteria": {
        "SeriesDescription": "Axial EPI-FMRI (Interleaved I to S)*"
      "sidecarChanges": {
        "TaskName": "rest"
      }
      }
    }
  ]
}
```

=== "Command"

    ```sh
    nano code/dcm2bids_config.json
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ nano code/dcm2bids_config.json
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ cat code/dcm2bids_config.json
    {
      "descriptions": [
        {
          "dataType": "func",
          "modalityLabel": "bold",
          "customLabels": "task-rest",
          "criteria": {
            "SeriesDescription": "*Axial EPI-FMRI (Interleaved I to S)*"
          },
          "sidecarChanges": {
            "TaskName": "rest"
          }
        }
      ]
    }
    ```

!!! warning "Avoid using filename as criteria"

    While you can take file names to match as criteria, we do not recommend this
    as different versions of dcm2niix can lead to different file names (Refer to
    the [release notes of version 17-March-2021 (v1.0.20210317)][dcm2niix-release]
    of dcmniix to now more, especially the [GE file naming behavior changes (%p protocol name and %d description) section](https://github.com/rordenlab/dcm2niix/issues/476).

Moving to the two fieldmaps, if you inspect their sidecar files (the same ones
that were compared in the
[dcm2bids_helper section](#finding-what-you-need-in-tmpdcm2bidshelper)), you can
see a pattern of `"EPI PE=AP"` or `"EPI PE=PA"` in the `SeriesDescription` once
again. Is it enough to match only the correct acquisition?

You can test it, of course!

=== "Command"

    ```sh
    grep "EPI PE=AP" tmp_dcm2bids/helper/*.json
    grep "EPI PE=PA" tmp_dcm2bids/helper/*.json
    ```

=== "Output"

    There are two matches per pattern but they come from the same file, so it is okay.
    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ grep "EPI PE=AP" tmp_dcm2bids/helper/*.json
    tmp_dcm2bids/helper/003_In_EPI_PE=AP_20180918121230.json:	"SeriesDescription": "EPI PE=AP",
    tmp_dcm2bids/helper/003_In_EPI_PE=AP_20180918121230.json:	"ProtocolName": "EPI PE=AP",
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ grep "EPI PE=PA" tmp_dcm2bids/helper/*.json
    tmp_dcm2bids/helper/004_In_EPI_PE=PA_20180918121230.json:	"SeriesDescription": "EPI PE=PA",
    tmp_dcm2bids/helper/004_In_EPI_PE=PA_20180918121230.json:	"ProtocolName": "EPI PE=PA",

    ```

Once you are sure of you matching criteria, you can update your configuration
file with the appropriate info.

```json hl_lines="21 30"
{
  "descriptions": [
    {
      "dataType": "func",
      "modalityLabel": "bold",
      "customLabels": "task-rest",
      "criteria": {
        "SeriesDescription": "Axial EPI-FMRI (Interleaved I to S)*"
      },
      "sidecarChanges": {
        "TaskName": "rest"
      }
    },
    {
      "dataType": "fmap",
      "modalityLabel": "epi",
      "customLabels": "dir-AP",
      "criteria": {
        "SeriesDescription": "EPI PE=AP*"
      },
      "intendedFor": 0
    },
    {
      "dataType": "fmap",
      "modalityLabel": "epi",
      "customLabels": "dir-PA",
      "criteria": {
        "SeriesDescription": "EPI PE=PA*"
      },
      "intendedFor": 0
    }
  ]
}
```

For fieldmaps, you need to add an `"intendedFor"` field to show that these
fieldmaps should be used with your fMRI acquisition. Have a look at the
explanation of [intendedFor](/docs/3-configuration/#intendedfor) in the
documentation or in the [BIDS specification][bids-fmap].

!!! tip "Use an online JSON validator"

    Editing JSON file is prone to errors such as misplacing or forgetting a comma or
    not having matched opening and closing `[]` or `{}`. JSON linters are useful to
    validate that we did enter all information successfully. You can find these
    tools online, for example <https://jsonlint.com>.

Now that you have a configuration file ready, it is time to finally run
`dcm2bids`.

## Running `dcm2bids`

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
    dcm2bids 2.1.7

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
    --forceDcm2niix       Overwrite previous temporary dcm2niix output if it exists
    --clobber             Overwrite output if it exists
    -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                            Set logging level
    -a, --anonymizer      This option no longer exists from the script in this release. See:https://github.com/unfmontreal/Dcm2Bids/blob/master/README.md#defaceTpl

                Documentation at https://github.com/unfmontreal/Dcm2Bids

    ```

As you can see, to run the `dcm2bids` command, you have to specify at least 3
required options with their argument.

```sh
dcm2bids -d path/to/source/data -p subject_id -c path/to/config/file.json
```

`dcm2bids` will create a directory which will be named after the argument
specified for `-p`, and put the _BIDSified_ data in it.

For the tutorial, pretend that the subject_id is simply `ID01`.

Note that if you don't specify the `-o` option, your current directory will be
populated with the `sub-<label>` directories.

That being said, you can run the command:

=== "Command"

    ```sh
    dcm2bids -d sourcedata/dcm_qa_nih/In/ -p ID01 -c code/dcm2bids_config.json
    ```

=== "Output"

    ```sh hl_lines="14-16"
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ dcm2bids -d sourcedata/dcm_qa_nih/In/ -p ID01 -c code/dcm2bids_config.json
    INFO:dcm2bids.dcm2bids:--- dcm2bids start ---
    INFO:dcm2bids.dcm2bids:OS:version: Linux-5.13.0-39-generic-x86_64-with-glibc2.31
    INFO:dcm2bids.dcm2bids:python:version: 3.10.4 | packaged by conda-forge | (main, Mar 24 2022, 17:39:04) [GCC 10.3.0]
    INFO:dcm2bids.dcm2bids:dcm2bids:version: 2.1.7
    INFO:dcm2bids.dcm2bids:dcm2niix:version: v1.0.20211006
    INFO:dcm2bids.dcm2bids:participant: sub-ID01
    INFO:dcm2bids.dcm2bids:session:
    INFO:dcm2bids.dcm2bids:config: /home/sam/dcm2bids-tutorial/bids_project/code/dcm2bids_config.json
    INFO:dcm2bids.dcm2bids:BIDS directory: /home/sam/dcm2bids-tutorial/bids_project
    INFO:dcm2bids.utils:Running dcm2niix -b y -ba y -z y -f '%3s_%f_%p_%t' -o /home/sam/dcm2bids-tutorial/bids_project/tmp_dcm2bids/sub-ID01 sourcedata/dcm_qa_nih/In/
    INFO:dcm2bids.dcm2niix:Check log file for dcm2niix output
    INFO:dcm2bids.sidecar:Sidecars pairing:
    INFO:dcm2bids.sidecar:_dir-AP_epi  <-  003_In_EPI_PE=AP_20180918121230
    INFO:dcm2bids.sidecar:_task-rest_bold  <-  004_In_DCM2NIIX_regression_test_20180918114023
    INFO:dcm2bids.sidecar:_dir-PA_epi  <-  004_In_EPI_PE=PA_20180918121230
    INFO:dcm2bids.sidecar:No Pairing  <-  005_In_DCM2NIIX_regression_test_20180918114023
    INFO:dcm2bids.sidecar:No Pairing  <-  005_In_EPI_PE=RL_20180918121230
    INFO:dcm2bids.sidecar:No Pairing  <-  006_In_DCM2NIIX_regression_test_20180918114023
    INFO:dcm2bids.sidecar:No Pairing  <-  006_In_EPI_PE=LR_20180918121230
    INFO:dcm2bids.sidecar:No Pairing  <-  007_In_DCM2NIIX_regression_test_20180918114023
    INFO:dcm2bids.dcm2bids:moving acquisitions into BIDS folder
    ```

A bunch of information is printed to the terminal as well as to a log file
located at `tmp_dcm2bids/log/sub-<label>_<datetime>.log`. It is useful to keep
these log files in case you notice an error after a while and need to find which
participants are affected.

You can see that dcm2bids was able to pair and match the files you specified at
lines 14-16 in the previous output tab.

You can now have a look in the newly created folder `sub-ID01` and discover your
converted data!

=== "Command"

    ```sh
    tree sub-ID01/
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ tree sub-ID01/
    sub-ID01/
    ├── fmap
    │   ├── sub-ID01_dir-AP_epi.json
    │   ├── sub-ID01_dir-AP_epi.nii.gz
    │   ├── sub-ID01_dir-PA_epi.json
    │   └── sub-ID01_dir-PA_epi.nii.gz
    └── func
        ├── sub-ID01_task-rest_bold.json
        └── sub-ID01_task-rest_bold.nii.gz

    2 directories, 6 files
    ```

Files that were not paired stay in a temporary directory
`tmp_dcm2bids/sub-<label>`. In your case : `tmp_dcm2bids/sub-ID01`.

=== "Command"

    ```sh
    tree tmp_dcm2bids/
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/dcm2bids-tutorial/bids_project$ tree tmp_dcm2bids/
    tmp_dcm2bids/
    ├── helper
    │   ├── 003_In_EPI_PE=AP_20180918121230.json
    │   ├── 003_In_EPI_PE=AP_20180918121230.nii.gz
    │   ├── 004_In_DCM2NIIX_regression_test_20180918114023.json
    │   ├── 004_In_DCM2NIIX_regression_test_20180918114023.nii.gz
    │   ├── 004_In_EPI_PE=PA_20180918121230.json
    │   ├── 004_In_EPI_PE=PA_20180918121230.nii.gz
    │   ├── 005_In_DCM2NIIX_regression_test_20180918114023.json
    │   ├── 005_In_DCM2NIIX_regression_test_20180918114023.nii.gz
    │   ├── 005_In_EPI_PE=RL_20180918121230.json
    │   ├── 005_In_EPI_PE=RL_20180918121230.nii.gz
    │   ├── 006_In_DCM2NIIX_regression_test_20180918114023.json
    │   ├── 006_In_DCM2NIIX_regression_test_20180918114023.nii.gz
    │   ├── 006_In_EPI_PE=LR_20180918121230.json
    │   ├── 006_In_EPI_PE=LR_20180918121230.nii.gz
    │   ├── 007_In_DCM2NIIX_regression_test_20180918114023.json
    │   └── 007_In_DCM2NIIX_regression_test_20180918114023.nii.gz
    ├── log
    │   └── sub-ID01_2022-04-19T111537.459742.log
    └── sub-ID01
        ├── 005_In_DCM2NIIX_regression_test_20180918114023.json
        ├── 005_In_DCM2NIIX_regression_test_20180918114023.nii.gz
        ├── 005_In_EPI_PE=RL_20180918121230.json
        ├── 005_In_EPI_PE=RL_20180918121230.nii.gz
        ├── 006_In_DCM2NIIX_regression_test_20180918114023.json
        ├── 006_In_DCM2NIIX_regression_test_20180918114023.nii.gz
        ├── 006_In_EPI_PE=LR_20180918121230.json
        ├── 006_In_EPI_PE=LR_20180918121230.nii.gz
        ├── 007_In_DCM2NIIX_regression_test_20180918114023.json
        └── 007_In_DCM2NIIX_regression_test_20180918114023.nii.gz

    3 directories, 27 files
    ```

That is it, you are done with the tutorial! You can now browse through the
documentation to find information about the different commands.

[Go to the How-to guides section :books: ](../../how-to/){ .md-button }

!!! cite "Acknowledgment"

    Thanks to @Remi-gau for letting us know that our tutorial needed an update, and for providing us with a clean and working configuration file through an [issue #142](https://github.com/UNFmontreal/Dcm2Bids/issues/142) on GitHub :pray:.

[bids-spec]: https://bids-specification.readthedocs.io/en/stable/
[bids-fmap]:
  https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#fieldmap-data
[dcm2niix-release]:
  https://github.com/rordenlab/dcm2niix/releases/tag/v1.0.20210317
[bids-starter-kit]: https://bids-standard.github.io/bids-starter-kit/
[bids-starter-kit-annot]:
  https://bids-standard.github.io/bids-starter-kit/tutorials/annotation.html
[dcm_qc_nih]: https://github.com/neurolabusc/dcm_qa_nih
[config]: ../how-to/create-config-file.md
