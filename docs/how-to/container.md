# dcm2bids with Docker and Apptainer / Singularity

We provide a container image that includes both dcm2niix and dcm2bids as well as pydeface and the BIDS validator. You can find it on [Docker Hub](https://hub.docker.com/r/unfmontreal/dcm2bids).

You can install it using [Docker](https://www.docker.com/get-started) or [Apptainer/Singularity](https://www.apptainer.org).

## Prerequisites

Before you begin, make sure you have at least one of the following installed:

- Docker: [Download and install Docker](https://www.docker.com/get-started)
- Apptainer, formerly known as Singularity : [Download and install Apptainer](https://apptainer.org/docs/admin/main/installation.html)

!!! note
    If you are using a HPC cluster, Apptainer is the recommended choice and is probably installed on your system. Simply load the module (e.g., 
    `module load apptainer`) and use the `apptainer` command,

## Step 1: Pull the dcm2bids container

To start, you can either pull the dcm2bids image from the Docker Hub repository or [build it from the Dockerfile in the repository](https://github.com/UNFmontreal/Dcm2Bids/blob/dev/Dockerfile).:

=== "Docker"

    ```
    docker pull unfmontreal/dcm2bids:latest
    ```

=== "Apptainer/Singularity"

    ```
    apptainer pull dcm2bids.sif docker://unfmontreal/dcm2bids:latest
    ```

## Step 2: Test dcm2bids

The default command, or the point of entry, for the container is `dcm2bids`. So every time you run the container, you can pass the `dcm2bids` arguments and options directly. To test the container, run the following command to display the help message for the `dcm2bids` command.

=== "Docker"

    ```
    docker run --rm -it unfmontreal/dcm2bids:latest --help
    ```

=== "Apptainer/Singularity"

    ```
    apptainer run dcm2bids.sif --help
    ```

## Step 3: Run `dcm2bids_scaffold`

To run `dcm2bids_scaffold`, `with singularity`, you need to *execute* a command instead of *running* the pre-specified command (`dcm2bids`). You need to bind the respective volumes.

=== "Docker"

    ```
    docker run --rm -it \
    --entrypoint /venv/bin/dcm2bids_scaffold \
    -v /path/to/output-dir:/output \
    unfmontreal/dcm2bids:latest -o /output/new_bids_dataset
    ```

=== "Apptainer/Singularity"

    ```
    singularity exec \
    -B /path/to/output-dir:/output \
    dcm2bids.sif dcm2bids_scaffold -o /output/new_bids_dataset
    ```


## Step 4: Run `dcm2bids_helper`

To run `dcm2bids_helper`, `with singularity`, you need to *execute* a command instead of *running* the pre-specified command (`dcm2bids`). To bind the respective volumes, you have two options:

1. Put the input data in the same parent directory as the output directory.
2. Specify the input data directory as a separate volume.

If you bind the newly scaffolded directory on its own, you can simply use the `-o /output` instead of having to specify the full path to the scaffolded directory. Same goes for the input data directory, if the input data directory is one subject, you can bind it directly to `/input`. If it is the parent directory of multiple subjects, you can bind it to `/input` and specify the specific subject directory (e.g, `-d /input/subject-01`).

=== "Docker"

    ```
    docker run --rm -it --entrypoint /venv/bin/dcm2bids_helper \
    -v /path/to/input-data:/input \
    -v /path/to/output-dir/new_bids_dataset:/output \
    unfmontreal/dcm2bids:latest -o /output -d /input
    ```

=== "Apptainer/Singularity"

    ```
    singularity exec \
    -B /path/to/input-data:/input \
    -B /path/to/output-dir/new_bids_dataset:/output \
    dcm2bids.sif dcm2bids_helper -o /output -d /input
    ```

## Step 5: Run `dcm2bids`

You can use `run` as in Step 2 or use `exec dcm2bids` to run `dcm2bids` with the appropriate arguments and options. You need to bind the respective volumes.

You can put input data in the same parent directory as the output directory, or you can specify the input data directory as a separate volume. You must also specify the path to the configuration file. If you use the scaffolded dataset, the config file is usually in the `code/` directory.

You can also [deface your data](use-advanced-commands.md#post_op) and [validate your BIDS data](use-advanced-commands.md#-bids_validate) using the `--bids_validate` flag.

=== "Docker"

    ```
    docker run --rm -it \
    -B /path/to/input-data:/input \
    -B /path/to/output-dir/new_bids_dataset:/output \
    unfmontreal/dcm2bids:latest --auto_extract_entities --bids_validate \
    -o /output -d /input -c /output/code/config.json -p 001
    ```

=== "Apptainer/Singularity"

    ```
    singularity run \
    -B /path/to/input-data:/input \
    -B /path/to/output-dir/new_bids_dataset:/output \
    dcm2bids.sif --auto_extract_entities --bids_validate \
    -o /output -d /input -c /output/code/config.json -p 001
    ```
