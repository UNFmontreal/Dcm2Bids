From ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive

MAINTAINER Arnaud Boré <arnaud.bore@gmail.com>

RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get -y install wget build-essential cmake git pigz \
               nodejs python3 python3-pip unzip

RUN pip3 install dcm2bids

# Install dcm2niix from github
ENV DCM2NIIX_VERSION="v1.0.20201102"

WORKDIR /usr/local/src
RUN git clone https://github.com/rordenlab/dcm2niix.git
WORKDIR /usr/local/src/dcm2niix
RUN git checkout tags/${DCM2NIIX_VERSION} -b install
RUN mkdir build
WORKDIR /usr/local/src/dcm2niix/build
RUN cmake ..
RUN make install

WORKDIR /
