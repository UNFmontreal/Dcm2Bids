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
    docker pull unfmontreal/dcm2bids:${VERSION}
    ```

=== "Apptainer/Singularity"

    ```
    apptainer pull dcm2bids_${VERSION}.sif docker://unfmontreal/dcm2bids:${VERSION}
    ```

## Step 2: Test dcm2bids

The default command, or the point of entry, for the container is `dcm2bids`. So every time you run the container, you can pass the `dcm2bids` arguments and options directly. To test the container, run the following command to display the help message for the `dcm2bids` command.

=== "Docker"

    ```
    docker run --rm -it unfmontreal/dcm2bids:latest --help
    ```

=== "Apptainer/Singularity"

    ```
    apptainer run -e --containall dcm2bids.sif --help
    ```

## Step 3: Run `dcm2bids_scaffold`

To run `dcm2bids_scaffold` with Apptainer/Singularity, you need to *execute* a command instead of *running* the pre-specified command (`dcm2bids`). You need to bind the respective volumes.

=== "Docker"

    ```
    docker run --rm -it \
    --entrypoint /venv/bin/dcm2bids_scaffold \
    -v /path/to/bids:/bids \
    unfmontreal/dcm2bids:${VERSION} -o /bids/new_scaffold
    ```

=== "Apptainer/Singularity"

    ```
    apptainer exec \
    -e --containall \
    -B /path/to/bids:/bids \
    dcm2bids.sif dcm2bids_scaffold -o /bids/new_scaffold
    ```


## Step 4: Run `dcm2bids_helper`

To run `dcm2bids_helper` with Apptainer/Singularity, you need to *execute* a command instead of *running* the pre-specified command (`dcm2bids`). To bind the respective volumes, you have two options:

1. Put the input data in the same parent directory as the output directory.
2. Specify the input data directory as a separate volume.

If you bind the newly scaffolded directory on its own, you can simply use the `-o /bids` instead of having to specify the full path to the scaffolded directory. Same goes for the input data directory, if the input data directory is one subject, you can bind it directly to `/dicoms`. If it is the parent directory of multiple subjects, you can bind it to `/dicoms` and specify the specific subject directory (e.g, `-d /dicoms/subject-01`).

=== "Docker"

    ```
    docker run --rm -it --entrypoint /venv/bin/dcm2bids_helper \
    -v /path/to/dicoms:/dicoms:ro \
    -v /path/to/bids/new_scaffold:/bids \
    unfmontreal/dcm2bids:${VERSION} -o /bids -d /dicoms
    ```

=== "Apptainer/Singularity"

    ```
    apptainer exec \
    -B /path/to/dicoms:/dicoms:ro \
    -B /path/to/bids/new_scaffold:/bids \
    dcm2bids.sif dcm2bids_helper -o /bids -d /dicoms
    ```

## Step 5: Run `dcm2bids`

You can use `run` as in Step 2 or use `exec dcm2bids` to run `dcm2bids` with the appropriate arguments and options. You need to bind the respective volumes.

You can put input data in the same parent directory as the output directory, or you can specify the input data directory as a separate volume. You must also specify the path to the configuration file. If you use the scaffolded dataset, the config file is usually in the `code/` directory.

You can also [deface your data](use-advanced-commands.md#post_op) and [validate your BIDS data](use-advanced-commands.md#-bids_validate) using the `--bids_validate` flag.

=== "Docker"

    ```
    docker run --rm -it \
    -v /path/to/dicoms:/dicoms:ro \
    -v /path/to/config.json:/config.json:ro \
    -v /path/to/bids/new_scaffold:/bids \
    unfmontreal/dcm2bids:${VERSION} --auto_extract_entities --bids_validate \
    -o /bids -d /dicoms -c /config.json -p 001
    ```

=== "Apptainer/Singularity"

    ```
    apptainer run \
    -B /path/to/dicoms:/dicoms:ro \
    -B /path/to/config.json:/config.json:ro \
    -B /path/to/bids/new_scaffold:/bids \
    dcm2bids.sif --auto_extract_entities --bids_validate \
    -o /bids -d /dicoms -c /config.json -p 001
    ```
