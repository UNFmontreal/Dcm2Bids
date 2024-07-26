# Tutorial - Convert multiple participants in parallel

## Motivation

Instead of manually converting one participant after the other, one could be
tempted to speed up the process. There are many ways to speed up the process and
using [GNU parallel][parallel] is one of them. [GNU parallel][parallel] provides
an intuitive and concise syntax, making it user-friendly even for those with
limited programming experience, just like dcm2bids 😄. By utilizing multiple
cores simultaneously, [GNU parallel][parallel] significantly speeds up the
conversion process, saving time and resources. In sum, by using [GNU
parallel][parallel], we can quickly and easily convert our data with minimal
effort and maximum productivity.

## Prerequisites

Before proceeding with this tutorial, there are a few things you need to have in
place:

- Be familiar with `dcm2bids` or, at least, have followed the
  [First steps tutorial](../first-steps);
- Have a [dcm2bids config file][config] ready or know how to make one;
- Have more than one participant's data to convert;
- Each participant's DICOM files should be organized into separate directories
  or archives.
  - Since version **3.1.0**, `dcm2bids` can use compressed archives or
    directories as input, it doesn't matter.

### Setup

!!! warning "dcm2bids and GNU parallel must be installed"

    If you have not installed dcm2bids yet, now is the time to go to the
    [installation page](../get-started/install.md) and install dcm2bids with its
    dependencies. This tutorial does not cover the installation part and assumes
    you have dcm2bids properly installed.

    [GNU parallel][parallel] may be already installed
    on your computer. If you can't run the command `parallel`, you can download it on
    [their website][parallel]. Note that if you installed
    dcm2bids in a **conda environment** you can also install parallel in it through the
    conda-forge channel. Once your env is activated, run `conda install -c conda-forge parallel`
    to install it.

### Verify dcm2bids and parallel version

First thing first, let's make sure our software are usable.

=== "Command"

    ```sh
    dcm2bids -v
    parallel --version
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~$ dcm2bids -v
    dcm2bids version:       3.1.0
    Based on BIDS version:  v1.9.0
    (dcm2bids) sam:~$ parallel --version
    GNU parallel 20230722
    Copyright (C) 2007-2023 Ole Tange, http://ole.tange.dk and Free Software
    Foundation, Inc.
    License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    GNU parallel comes with no warranty.

    Web site: https://www.gnu.org/software/parallel

    When using programs that use GNU Parallel to process data for publication
    please cite as described in 'parallel --citation'.
    ```

If you don't see a similar output, it is likely an installation issue or the
software were not added to your system's PATH. This allows you to easily execute
dcm2bids commands without specifying the full path to the executables. If you
are using a virtual env or conda env, make sure it is _activated_.

## Create scaffold

We will first use the `dcm2bids_scaffold` command to create basic BIDS files and
directories. It is based on the material provided by the [BIDS starter
kit][bids-starter-kit]. This ensures we have a valid BIDS structure to start
with.

=== "Command"

    ```sh
    dcm2bids_scaffold -o name_of_your_bids_dir
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~$ dcm2bids_scaffold -o tuto-parallel
    INFO    | --- dcm2bids_scaffold start ---
    INFO    | Running the following command: /home/sam/miniconda3/envs/dcm2bids/bin/dcm2bids_scaffold -o tuto-parallel
    INFO    | OS version: Linux-5.15.0-83-generic-x86_64-with-glibc2.31
    INFO    | Python version: 3.10.4 | packaged by conda-forge | (main, Mar 24 2022, 17:39:04) [GCC 10.3.0]
    INFO    | dcm2bids version: 3.1.0
    INFO    | Checking for software update
    INFO    | Currently using the latest version of dcm2bids.
    INFO    | The files used to create your BIDS directory were taken from https://github.com/bids-standard/bids-starter-kit.

    INFO    | Tree representation of tuto-parallel/
    INFO    | tuto-parallel/
    INFO    | ├── code/
    INFO    | ├── derivatives/
    INFO    | ├── sourcedata/
    INFO    | ├── tmp_dcm2bids/
    INFO    | │   └── log/
    INFO    | │       └── scaffold_20230913-095334.log
    INFO    | ├── .bidsignore
    INFO    | ├── CHANGES
    INFO    | ├── dataset_description.json
    INFO    | ├── participants.json
    INFO    | ├── participants.tsv
    INFO    | └── README
    INFO    | Log file saved at tuto-parallel/tmp_dcm2bids/log/scaffold_20230913-095334.log
    INFO    | --- dcm2bids_scaffold end ---
    ```

## Populate the `sourcedata` directory

This step is optional but it makes things easier when all the data are within
the same directory. The `sourcedata` directory is meant to contain your DICOM
files. It doesn't mean you have to duplicate your files there but it is nice to
[symlink](https://en.wikipedia.org/wiki/Symbolic_link) them there. That being
said, feel free to let your DICOM directories wherever they are, and use that
as an input to your dcm2bids command.

=== "Command"

    ```sh
    ln -s TARGET DIRECTORY
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/tuto-parallel$ ln -s $HOME/data/punk_proj/ sourcedata/
    (dcm2bids) sam:~/tuto-parallel$ tree sourcedata/
    sourcedata/
    └── punk_proj -> /home/sam/data/punk_proj/

    1 directory, 0 files
    (dcm2bids) sam:~/tuto-parallel$ ls -1 sourcedata/punk_proj/
    PUNK041.tar.bz2
    PUNK042.tar.bz2
    PUNK043.tar.bz2
    PUNK044.tar.bz2
    PUNK045.tar.bz2
    PUNK046.tar.bz2
    PUNK047.tar.bz2
    PUNK048.tar.bz2
    PUNK049.tar.bz2
    PUNK050.tar.bz2
    PUNK051.tar.bz2
    ```

Now that I can access all the _punk_ subjects from within the `sourcedata` as
`sourcedata/punk_proj/` points to its target.

## Get your config file ready and test it

You can either run `dcm2bids_helper` to help build your config file or import
one if your already have one. The config file is necessary for specifying the
conversion parameters and mapping the metadata from DICOM to BIDS format.

Because the tutorial is about `parallel`, I simply copied a config file I
created for my data to `code/config_dcm2bids_t1w.json`. This config file aims to
**BIDSify** and **deface** T1w found for each participant.

```json title="config_dcm2bids_t1w.json"
{
  "post_op": [
    {
      "cmd": "pydeface --outfile dst_file src_file",
      "datatype": "anat",
      "suffix": ["T1w"],
      "custom_entities": "rec-defaced"
    }
  ],
  "descriptions": [
    {
      "datatype": "anat",
      "suffix": "T1w",
      "criteria": {
        "SeriesDescription": "anat_T1w"
      }
    }
  ]
}
```

Make sure that your config file runs successfully on one participant at least
before moving onto parallelizing.

In my case,
`dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK041.tar.bz2 -p 041`
ran without any problem.

## Running parallel

Running pydeface takes quite a long time to run on a single participant. Instead
of running participant serially as with a `for loop`, `parallel` can be used to
run as many as your machine can at once.

### From a single subject to several at once

If you have never heard of parallel, here's how the maintainers describes the
tool:

> GNU parallel is a shell tool for executing jobs in parallel using one or more
> computers. A job can be a single command or a small script that has to be run
> for each of the lines in the input. The typical input is a list of files, a
> list of hosts, a list of users, a list of URLs, or a list of tables. A job can
> also be a command that reads from a pipe. GNU parallel can then split the
> input and pipe it into commands in parallel.

#### Understanding how parallel works

In order to use parallel, we have to give it a list of our subjects we want to
convert. You can generate this list by hand, in a text file or through a first
command that you will pipe to parallel.

Here's a basic example to list all the punk_proj participants and run `echo` on
each of them.

=== "Command"

    ```sh
    ls PATH/TO/YOUR/SOURCE/DATA | parallel echo "This is the command for subject {}"
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/tuto-parallel$ ls sourcedata/punk_proj | parallel echo "This is the command for subject {}"
    This is the command for subject PUNK041.tar.bz2
    This is the command for subject PUNK042.tar.bz2
    This is the command for subject PUNK043.tar.bz2
    This is the command for subject PUNK044.tar.bz2
    This is the command for subject PUNK045.tar.bz2
    This is the command for subject PUNK046.tar.bz2
    This is the command for subject PUNK047.tar.bz2
    This is the command for subject PUNK048.tar.bz2
    This is the command for subject PUNK049.tar.bz2
    This is the command for subject PUNK050.tar.bz2
    This is the command for subject PUNK051.tar.bz2
    ```

However, if you want to do something with the files, you have to be more
specific, otherwise the program won't find the file because the relative path is
not specified as shown below. However, keep in mind that having just the
filenames is also worth it as they contains really important information that we
will need, namely the participant ID. We will eventually extract it.

=== "Command"

    ```sh
    ls PATH/TO/YOUR/SOURCE/DATA | parallel ls {}
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/tuto-parallel$ ls sourcedata/punk_proj | parallel ls {}
    ls: cannot access 'PUNK041.tar.bz2': No such file or directory
    ls: cannot access 'PUNK042.tar.bz2': No such file or directory
    ls: cannot access 'PUNK043.tar.bz2': No such file or directory
    ls: cannot access 'PUNK044.tar.bz2': No such file or directory
    ls: cannot access 'PUNK045.tar.bz2': No such file or directory
    ls: cannot access 'PUNK046.tar.bz2': No such file or directory
    ls: cannot access 'PUNK047.tar.bz2': No such file or directory
    ls: cannot access 'PUNK048.tar.bz2': No such file or directory
    ls: cannot access 'PUNK049.tar.bz2': No such file or directory
    ls: cannot access 'PUNK050.tar.bz2': No such file or directory
    ls: cannot access 'PUNK051.tar.bz2': No such file or directory
    ```

You can solve this by simply adding the path to the ls command (e.g.,
`ls sourcedata/punk_proj/*`) or by using the parallel `:::` as input source:

=== "Command"

    ```sh
    parallel ls {} ::: PATH/TO/YOUR/SOURCE/DATA/*
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/tuto-parallel$ parallel ls {} ::: sourcedata/punk_proj/*
    sourcedata/punk_proj/PUNK041.tar.bz2
    sourcedata/punk_proj/PUNK042.tar.bz2
    sourcedata/punk_proj/PUNK043.tar.bz2
    sourcedata/punk_proj/PUNK044.tar.bz2
    sourcedata/punk_proj/PUNK045.tar.bz2
    sourcedata/punk_proj/PUNK046.tar.bz2
    sourcedata/punk_proj/PUNK047.tar.bz2
    sourcedata/punk_proj/PUNK048.tar.bz2
    sourcedata/punk_proj/PUNK049.tar.bz2
    sourcedata/punk_proj/PUNK050.tar.bz2
    sourcedata/punk_proj/PUNK051.tar.bz2
    ```

### Extracting participant ID with parallel

Depending on how standardized your participants' directory name are, you may
have spend a little bit of time figuring out the best way to extract the
participant ID from the directory name. This means you might have to read the
parallel help pages to dig through examples to find your case scenario.

If you are lucky, all the names are already standardized in addition to being
BIDS-compliant already.

In my case, I can use the `--plus` flag directly in parallel to extract the
alphanum pattern I wanted to keep by using `{/..}` (basename only) or a perl
expression to perform string replacements. Another common case if you want only
the digit from file names (or compressed archives without number) would be to
use `{//[^0-9]/}`.

=== "Command"

    ```sh
    parallel --plus echo data path: {} and fullname ID: {/..} VS digit-only ID: "{= s/.*\\/YOUR_PATTERN_BEFORE_ID//; s/TRAILING_PATH_TO_BE_REMOVED// =}" ::: PATH/TO/YOUR/SOURCE/DATA/*
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/tuto-parallel$ parallel --plus echo data path: {} and fullname ID: {/..} VS digit-only ID: "{= s/.*\\/PUNK//; s/.tar.*// =}" ::: sourcedata/punk_proj/*
    data path: sourcedata/punk_proj/PUNK041.tar.bz2 and fullname ID: PUNK041 VS digit-only ID: 041
    data path: sourcedata/punk_proj/PUNK042.tar.bz2 and fullname ID: PUNK042 VS digit-only ID: 042
    data path: sourcedata/punk_proj/PUNK043.tar.bz2 and fullname ID: PUNK043 VS digit-only ID: 043
    data path: sourcedata/punk_proj/PUNK044.tar.bz2 and fullname ID: PUNK044 VS digit-only ID: 044
    data path: sourcedata/punk_proj/PUNK045.tar.bz2 and fullname ID: PUNK045 VS digit-only ID: 045
    data path: sourcedata/punk_proj/PUNK046.tar.bz2 and fullname ID: PUNK046 VS digit-only ID: 046
    data path: sourcedata/punk_proj/PUNK047.tar.bz2 and fullname ID: PUNK047 VS digit-only ID: 047
    data path: sourcedata/punk_proj/PUNK048.tar.bz2 and fullname ID: PUNK048 VS digit-only ID: 048
    data path: sourcedata/punk_proj/PUNK049.tar.bz2 and fullname ID: PUNK049 VS digit-only ID: 049
    data path: sourcedata/punk_proj/PUNK050.tar.bz2 and fullname ID: PUNK050 VS digit-only ID: 050
    data path: sourcedata/punk_proj/PUNK051.tar.bz2 and fullname ID: PUNK051 VS digit-only ID: 051
    ```

### Building the dcm2bids command with parallel

Once we know how to extract the participant ID, all we have left to do is to
build the command that will be used in parallel. One easy way to build our
command is to use the `--dry-run` flag.

=== "Command"

    ```sh
    parallel --dry-run --plus dcm2bids --auto_extract_entities -c path/to/your/config.json -d {} -p "{= s/.*\\/YOUR_PATTERN_BEFORE_ID//; s/TRAILING_PATH_TO_BE_REMOVED// =}" ::: PATH/TO/YOUR/SOURCE/DATA/*
    ```

=== "Output"

    ```sh
    (dcm2bids) sam:~/tuto-parallel$ parallel --dry-run --plus dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d {} -p "{= s/.*\\/PUNK//; s/.tar.*// =}" ::: sourcedata/punk_proj/*
    dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK041.tar.bz2 -p 041
    dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK042.tar.bz2 -p 042
    dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK043.tar.bz2 -p 043
    dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK044.tar.bz2 -p 044
    dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK045.tar.bz2 -p 045
    dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK046.tar.bz2 -p 046
    dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK047.tar.bz2 -p 047
    dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK048.tar.bz2 -p 048
    dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK049.tar.bz2 -p 049
    dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK050.tar.bz2 -p 050
    dcm2bids --auto_extract_entities -c code/config_dcm2bids_t1w.json -d sourcedata/punk_proj/PUNK051.tar.bz2 -p 051
    ```

### Launching parallel

Once you are sure that the dry-run is what you would like to run, you simply
have to remove the `--dry-run` flag and go for walk since the wait time may be
long, especially if pydeface has to run.

If you want to see what is happening, you can add the `--verbose` flag to the
parallel command so you will see what jobs are currently running.

Parallel will try to use as much cores as it can by default. If you need to
limit the number of jobs to be parallelize, you can do so by using the
`--jobs <number>` option. `<number>` is the number of cores you allow parallel
to use concurrently.

```sh
parallel --verbose --jobs 3 dcm2bids [...]
```

### Verifying the logs

Once all the participants have been converted, it is a good thing to analyze the
dcm2bids logs inside the `tmp_dcm2bids/log/`. They all follow the same pattern,
so it is easy to `grep` for specific error or warning messages.

```sh
grep -ri "error" tmp_dcm2bids/log/
grep -ri "warning" tmp_dcm2bids/log/
```

[bids-starter-kit]: https://bids-standard.github.io/bids-starter-kit/
[config]: ../how-to/create-config-file.md
[parallel]: https://www.gnu.org/software/parallel/
