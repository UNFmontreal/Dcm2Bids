# Conda image for installing FSL tools
FROM continuumio/miniconda3:26.3.2 AS build

# Install FSL tools with conda
COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

# Install and use conda-pack
RUN conda install -c conda-forge conda-pack
RUN conda-pack -n fsl -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar
RUN /venv/bin/conda-unpack
RUN conda install -p /venv pip

# Install bids-validator
RUN conda install -c conda-forge deno
RUN deno install -ERWN -g -n bids-validator-deno jsr:@bids/validator@2.4.1

# Install dcm2bids
RUN conda install pip
WORKDIR /
ADD . /dcm2bids
WORKDIR /dcm2bids
RUN /venv/bin/python -m pip install .

RUN /venv/bin/python -m pip install pydeface

# Runtime image for executing FSL tools
FROM debian:stable AS runtime

# Copy the conda env from previous stage
COPY --from=build /venv /venv
COPY --from=build /opt/conda/bin/deno /usr/local/bin/deno
COPY --from=build /root/.deno /root/.deno
COPY --from=build /root/.cache/deno /root/.cache/deno

# Point to conda executables
ENV PATH="/venv/bin:/root/.deno/bin:$PATH"

# Set FSL variables
ENV FSLDIR="/venv" 
ENV FSLCONFDIR="${FSLDIR}/config"
ENV FSLOUTPUTTYPE="NIFTI"
ENV FSLMULTIFILEQUIT="TRUE"
ENV FSLTCLSH="${FSLDIR}/bin/fsltclsh"
ENV FSLWISH="${FSLDIR}/bin/fslwish"
ENV FSLGECUDAQ="cuda.q"

# Update and install some utils
RUN apt-get -y update && apt-get -y install dc wget npm unzip

# Fetch data
RUN wget -P ${FSLDIR}/data https://git.fmrib.ox.ac.uk/fsl/data_standard/-/raw/master/MNI152_T1_1mm_brain.nii.gz

# Install dcm2niix
WORKDIR /
RUN wget https://github.com/rordenlab/dcm2niix/releases/download/v1.0.20260416/dcm2niix_lnx.zip
RUN unzip dcm2niix_lnx.zip
RUN mv dcm2niix /usr/bin/

#ENTRYPOINT ["dcm2bids"]