From python:3.7

RUN apt-get update
RUN apt-get -y upgrade

WORKDIR /
ENV DCM2BIDS_VERSION="master"
RUN wget https://github.com/UNFmontreal/Dcm2Bids/archive/${DCM2BIDS_VERSION}.zip
RUN unzip ${DCM2BIDS_VERSION}.zip
RUN mv Dcm2Bids-${DCM2BIDS_VERSION} dcm2bids

WORKDIR /dcm2bids
RUN pip install -e .
