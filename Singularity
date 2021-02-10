Bootstrap: debootstrap
OSVersion: focal
MirrorURL: http://us.archive.ubuntu.com/ubuntu/


%help
Launching dcm2bids with singularity:
    singularity exec <container>.simg dcm2bids [args]

Info: https://github.com/unfmontreal/Dcm2Bids


%labels
Maintainer Arnaud Boré <arnaud.bore@gmail.com>

%post
    #Dependencies
    sed -i 's/$/ universe/' /etc/apt/sources.list
    apt update && apt upgrade
    apt install -y build-essential cmake git pigz \
                   nodejs npm python3 python3-pip
    apt clean && apt autoclean && apt autoremove -y
    pip3 install --upgrade pip

    #Install bids-validator
    npm install -g bids-validator

    #Install dcm2niix from github
    cd /usr/local/src
    git clone https://github.com/rordenlab/dcm2niix.git
    cd dcm2niix
    git checkout tags/v1.0.20181125 -b install
    mkdir build && cd build
    cmake ..
    make install

    #Install dcm2bids from github
    cd /usr/local/src
    git clone https://github.com/unfmontreal/Dcm2Bids.git
    cd Dcm2Bids && pip install .


%runscript
    exec dcm2bids "$@"
