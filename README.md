# dcm2bids

<p>
<a href="https://pypi.org/project/dcm2bids">
<img alt="PyPI version" src="https://badge.fury.io/py/dcm2bids.svg">
</a>
<a href="https://unfmontreal.github.io/Dcm2Bids">
<img alt="Documentation" src="https://img.shields.io/badge/documentation-dcm2bids-succes.svg">
</a>
<a href="https://zenodo.org/badge/latestdoi/59581295">
<img alt="DOI" src="https://zenodo.org/badge/doi/10.5281/zenodo.2616548.svg">
</a>
<!--
<a href="https://singularity-hub.org/collections/544">
<img alt="Singularity Hub" src="https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg">
</a>
-->
</p>

<p>
<a href="https://github.com/unfmontreal/Dcm2Bids/actionsk">
<img alt="" src="https://github.com/unfmontreal/Dcm2Bids/workflows/Tests/badge.svg">
</a>
<a href="https://codecov.io/gh/unfmontreal/Dcm2Bids">
<img src="https://codecov.io/gh/unfmontreal/Dcm2Bids/branch/master/graph/badge.svg"/>
</a>
<a href="https://github.com/psf/black">
<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>
</p>

`dcm2bids` reorganises NIfTI files from [dcm2niix][dcm2niix-github] into the [Brain Imaging Data Structure][bids] (BIDS).

Before using this software, learn more about BIDS:

- read the BIDS [specifications][bids-spec] and the [paper][bids-nature]
- some dataset [examples][bids-examples]

## Dependencies

- [dcm2niix][dcm2niix-github] to convert DICOM to NIfTI. **You need to install it**
    - [install instructions][dcm2niix-install]
    - [Recent release][dcm2niix-release]

## Install

`pip install dcm2bids`

## Upgrading

`pip install --upgrade dcm2bids`

## TL;DR

1. `mkdir <YOUR_FUTURE_BIDS_FOLDER>`
2. `cd <YOUR_FUTURE_BIDS_FOLDER>`
3. `dcm2bids_scaffold`
4. `dcm2bids_helper -d <FOLDER_WITH_DICOMS_OF_A_TYPICAL_SESSION>`
5. Build your configuration file with the help of the content of `tmp_dcm2bids/helper`
6. `dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -c CONFIG_FILE` for each participants of your study

Follow the [tutorial](https://unfmontreal.github.io/Dcm2Bids/tutorial)

dcm2bids creates log files inside `<YOUR_FUTURE_BIDS_FOLDER>/tmp_dcm2bids/log`

## bids-validator

Run the [bids-validator][bids-validator] to check your directory. Don't forget to create a `.bidsignore` file at the root of your BIDS directory with `tmp_dcm2bids/*` inside.

## Similar projects

Other tools to create [BIDS][bids] datasets :

- [heudiconv][link-heudiconv]
- [bidskit][link-bidskit]
- [dac2bids][link-dac2bids]

[bids]: http://bids.neuroimaging.io/
[bids-examples]: https://github.com/bids-standard/bids-examples
[bids-nature]: https://www.nature.com/articles/sdata201644
[bids-spec]: https://bids-specification.readthedocs.io/en/stable/
[bids-validator]: https://github.com/bids-standard/bids-validator
[dcm2bids-doc]: https://unfmontreal.github.io/Dcm2Bids
[dcm2niix-github]: https://github.com/rordenlab/dcm2niix
[dcm2niix-install]: https://github.com/rordenlab/dcm2niix#install
[dcm2niix-release]: https://github.com/rordenlab/dcm2niix/releases
[link-heudiconv]: https://github.com/nipy/heudiconv
[link-bidskit]: https://github.com/jmtyszka/bidskit
[link-dac2bids]: https://github.com/dangom/dac2bids
