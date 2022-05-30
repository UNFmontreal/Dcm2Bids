---
summary: Set of instructions to help install dcm2bids and dependencies.
authors:
  - Samuel Guay
date: 2022-04-17
---

# Installation

Before you can use dcm2bids, you will need to get it installed. This page guides
you through a minimal, typical dcm2bids installation workflow that is sufficient
to complete all dcm2bids tasks.

We recommend to skim-read the full page **before** you start installing anything
considering there are many ways to install software in the Python ecosystem
which are often dependent on the familiarity and preference of the user.

We offer recommendations at the bottom of the page that will take care of the
whole installation process in one go and make use of a dedicated environment for
dcm2bids.

??? tip "You just want the installation command?"

    If you are used to installing packages, you can get it from PyPI or conda:

    `pip install dcm2bids`

    `conda install -c conda-forge dcm2bids`

## Dependencies

### Python

As dcm2bids is a Python package, the first prerequisite is that Python must be
installed on the machine you will use dcm2bids. You will need **Python 3.7 or
above** to run dcm2bids properly.

If you are unsure what version(s) of Python is available on your machine, you
can find out by opening a terminal and typing `python --version` or `python`.
The former will output the version directly in the terminal while the latter
will open an interactive Python shell with the version displayed in the first
line.

=== "python --version"

    ```bash hl_lines="2"
    sam:~$ python --version
    Python 3.10.4
    ```

=== "python"

    ```bash hl_lines="2"
    sam:~$ python
    Python 3.10.4 | packaged by conda-forge | (main, Mar 24 2022, 17:39:04) [GCC 10.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> exit()
    ```

If your system-wide version of Python is lower 3.7, it is okay. We will make
sure to use a higher version in the isolated environment that will be created
for dcm2bids. The important part is to verify that Python is installed.

If you are a **beginning user** in the Python ecosystem, the odds are that you
have installed [Anaconda][anaconda], which contains all Python versions so you
should be good. If you were not able to find out which version of Python is
installed on your machine or find Anaconda on your machine, we recommend that
you install Python through [Anaconda][anaconda].

??? question "Should I install Anaconda or Miniconda?"

    If you unsure what to install read this [section describing the differences between Anaconda and Miniconda][mini-vs-ana] to help you choose.

### dcm2niix

[dcm2niix][dcm2niix] can also be installed in a variety of ways as seen on [the
main page of the software][dcm2niix-install].

Whether you want to install the latest compiled executable directly on your
machine is up to you but you have to **make sure you can call the software from
any directory**. In other words, you have to make sure it is included in your
`$PATH`. Otherwise, dcm2bids won't be able to run dcm2niix for you. That's why
we recommend to install it at the same time in the dedicated environment.

As you can see, dcm2niix is available through [conda][conda] so that is the
approach chosen in this guide. We will benefit from the simplicity of installing
all software from the same located at. Steps to install dcm2niix are included in
the next secton.

## Recommendations

We recommend to install all the dependencies at once when installing dcm2bids on
a machine or server. As mentioned above the minimal installation requires only
dcm2bids, dcm2niix and Python >= 3.7. For ease of use and to make sure we have a
reproducible environment, we recommend to use a dedicated environment through
[conda][conda] or, for those who have it installed, [Anaconda][anaconda]. Note
that you **don't need** to use specifically them to use dcm2bids, but it will
make your life easier.

??? info "More info on conda"

    Conda is an open-source package management system and environment management
    system that runs on Windows, macOS, and Linux. Conda quickly installs, runs, and
    updates packages and their dependencies. Conda easily creates, saves, loads, and
    switches between environments on your local computer. The conda package and
    environment manager is included in all versions of Anaconda and Miniconda.
    - [conda docs](https://docs.conda.io/projects/conda/en/latest/)

??? question "But I use another package/env management system, what do I do?"

    Of course you can use your preferred package/env management system, whether it
    is venv, virtualenv, pyenv, pip, poetry, etc. This guide was built on the
    basis that no previous knowledge is required to install and learn dcm2bids by so
    providing a simple way to install dcm2bids without having to worry about the
    rest.

??? question "I already created an environment for my project, what do I do?"

    You can update your environment either by:

    1. installing dcm2bids while your environment is active like any package; or
    2. adding dcm2bids to the dependencies and updating your environment

    Here's an example with conda after updating an `environment.yml` file:

    ```bash
    conda env update --file environment.yml --prune
    ```

### Install dcm2bids

From now on, it is assumed that [conda][conda] (or [Anaconda][anaconda]) is
installed and correctly setup on your computer as it is the easiest way to
install dcm2bids and its dependencies on any OS. We assume that if you want to
install it in a different way, you have enough skills to do it on your own.

If you installed Anaconda and want to use the graphical user interface (GUI), you can follow the steps as
demonstrated below and only read the steps until the end of the installation guide.

??? info "Create your environment with the **Anaconda Navigator** GUI"

    1. Open Anaconda Navigator
    2. Click on Environments, then the + button at the bottom
        ![ana_navigator_1](https://user-images.githubusercontent.com/30598330/164787321-3748093a-81af-4368-8afd-12fc5bb2eb78.png#border)
    3. Enter the name of the environment, it can be anything. You can call it **dcm2bids** then select **Python**
        ![ana_navigator_2](https://user-images.githubusercontent.com/30598330/164787449-aab75a92-53ff-465a-bb92-7f1016b99ca8.png#border)
    4. Click on the new **dcm2bids** environment, then on **Channels**
    5. If you only see defaults, click on **Add...** then enter **conda-forge** then click on **Update channels**
    ![ana_navigator_3](https://user-images.githubusercontent.com/30598330/164787845-f2847217-8a6c-421b-9ba1-9369d24f3d27.png#border)
    1. You now need to add the two main software, so you need to search for them in the top right corner. You should see them appear as soon as you right **dcm2**. You can select both at the same time.
        * If you don't seem them, you probabble need to select **All** channels instead of **Installed**.
    ![ana_navigator_4](https://user-images.githubusercontent.com/30598330/164788061-5dfbdf15-f76e-4548-a8c6-9e0ae2bbff00.png#border)
    1. It will ask you to install a bunch of packages, **Apply**.
        ![ana_navigator_5](https://user-images.githubusercontent.com/30598330/164788227-a6d733c7-301d-4c9c-8b5f-20559dd32a45.png#border)
    2. You environment should now be ready, click on the green circle with the white arrow to start the environment. A terminal window should open.
    ![ana_navigator_6](https://user-images.githubusercontent.com/30598330/164788461-371c3744-e91d-4eea-a510-e6b4d4604c80.png#border)
    1. You should see the name of your environment **(dcm2bids)** to the left. You can now test that dcm2bids works.
    ![ana_navigator_7](https://user-images.githubusercontent.com/30598330/164788542-f076ae52-20f2-4e92-90b7-c27973b6c5ef.png#border)

We could install all the software one by one using a series of command:

```bash
conda install -c conda-forge dcm2bids
conda install -c conda-forge dcm2niix
```

But this would install the software in the main environment instead of a
dedicated one, assuming none were active. This could have atrocious dependencies
issues in the long-term if you want to install other software.



#### Create environment.yml

That is exactly why dedicated environments were invented. To help creating
dedicated environments, we can create a file, often called `environment.yml`,
which is used to specify things such as the dependencies that need to be
installed inside the environment.

To create such a file, you can use any code editor or your terminal to write or
paste the information below, and save it in your project directory with the name
`environment.yml`:

You can create a project directory anywhere on your computer, it does not
matter. You can create `dcm2bids-proj` if you need inspiration.

```yaml
name: dcm2bids
channels:
  - conda-forge
dependencies:
  - python>=3.7
  - dcm2niix
  - dcm2bids
```

In short, here's what the fields mean:

- The `name:` key refers to the name of the dedicated environment. You will have
  to use this name to activate your environment and use software installed
  inside. The name is arbitrary, you can name it however you want.
- The `channels:` key tells conda where to look for the declared dependencies.
  In our case, all our dependencies are located on the [conda-forge
  channel][conda-forge].
- The `dependencies:` key lists all the dependencies to be installed inside the
  environment. If you are creating an environment for your analysis project,
  this is where you would list other dependencies such as `nilearn`, `pandas`,
  and especially as `pip` since you don't want to use the pip outside of your
  environment Note that we specify `python>=3.7` to make sure the requirement is
  satisfied for dcm2bids as the newer version of dcm2bids may face issue with
  Python 3.6 and below.

Now that all the dependencies have been specified, it is time to create the new
conda environment dedicated to dcm2bids! :tada:

#### Create conda environment + install dcm2bids

Open a terminal and go in the directory where you put the `environment.yml` run
this command:

```bash
conda env create --file environment.yml
```

If the executation was successful, you should see a message similar to:

```bash hl_lines="14"
sam:~/dcm2bids-proj$ nano environment.yml
sam:~/dcm2bids-proj$ conda env create --file environment.yml
Collecting package metadata (repodata.json): done
Solving environment: |done

Downloading and Extracting Packages
future-0.18.2        | 738 KB    | ########################################## | 100%
Preparing transaction: done
Verifying transaction: done
Executing transaction: done
#
# To activate this environment, use
#
#     $ conda activate dcm2bids
#
# To deactivate an active environment, use
#
#     $ conda deactivate
```

#### Activate environment

Last step is to make sure you can activate[^1] your environment by running the
command:

```bash
conda activate dcm2bids
```

:warning: Remember that dcm2bids here refer to the name given specified in the
`environment.yml`.

```bash hl_lines="2"
sam:~/dcm2bids-proj$ conda activate dcm2bids
(dcm2bids) sam:~/dcm2bids-proj$
```

You can see the environment is activated as a new `(dcm2bids)` appear in front
of the username.

#### Verify that dcm2bids works

Finally, you can test that dcm2bids was installed correctly by running the any
dcm2bids command such as `dcm2bids --help`:

```bash hl_lines="1"
(dcm2bids) sam:~/dcm2bids-proj$ dcm2bids --help
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
                        (/home/sam/dcm2bids-proj)
  --forceDcm2niix       Overwrite previous temporary dcm2niix output if it exists
  --clobber             Overwrite output if it exists
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set logging level
  -a, --anonymizer      This option no longer exists from the script in this
                        release. See:https://github.com/unfmontreal/Dcm2Bids/blob/m
                        aster/README.md#defaceTpl

            Documentation at https://github.com/unfmontreal/Dcm2Bids
```

Voilà, you are ready to use dcm2bids or at least
[move onto the tutorial](../tutorial/first-steps.md)!!

[Go to the Tutorial section](../../tutorial){ .md-button }

[Go to the How-to section](../../how-to/){ .md-button }

## Containers

We also provide a container image that includes both dcm2niix and dcm2bids which
you can install using [Docker][docker] or [Apptainer/Singularity][apptainer].

=== "Docker"

    `docker pull unfmontreal/dcm2bids:latest`

=== "Apptainer/Singularity"

    `singularity pull dcm2bids_latest.sif docker://unfmontreal/dcm2bids:latest `

## Summary of the steps

In sum, installing dcm2bids is quite easy if you know how to install Python
packages. The easiest way to install it is to follow the steps below using
[conda][conda] but it is also possible to use other software, including
containers:

<!-- prettier-ignore-start -->

- [ ] Create an [`environment.yml`](#create-environmentyml) file with
      dependencies

    - [x] Content:

            name: dcm2bids
            channels:
                - conda-forge
            dependencies:
                - python>=3.7
                - dcm2niix
                - dcm2bids


- [ ] Create conda environment
    - [x] `conda env create --file environment.yml`
- [ ] Activate conda environment
    - [x] `conda activate dcm2bids`
- [ ] Verify a dcm2bids command
    - [x] `dcm2bids --help`
- [ ] Consult how-to guides or follow the tutorial

<!-- prettier-ignore-end -->

[anaconda]: https://www.anaconda.com/distribution
[dcm2niix]: https://github.com/rordenlab/dcm2niix
[dcm2niix-install]: https://github.com/rordenlab/dcm2niix#install
[conda]: https://conda.io/en/latest/miniconda.html
[conda-forge]: https://anaconda.org/conda-forge
[docker]: https://docker.com
[apptainer]: https://apptainer.org
[mini-vs-ana]:
  https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html#anaconda-or-miniconda

[^1]:
    To get out of a conda environment, you have to deactivate it with the
    `conda deactivate` command.
