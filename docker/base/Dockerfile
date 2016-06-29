FROM ubuntu:16.04
MAINTAINER Brian Van Klaveren <bvan@slac.stanford.edu>

RUN apt-get -y update &&\
        apt-get -y upgrade &&\
        apt-get --yes install bash \
        bison \
        bzip2 \
        cmake \
        curl \
        flex \
        g++ \
        gettext \
        git \
        libbz2-dev \
        libglib2.0-dev \
        libpthread-workqueue-dev \
        libreadline-dev \
        libssl-dev \
        libsm6 \
        make \
        python-numpy \
        ncurses-dev \
        openjdk-8-jre-headless \
        openssl \
        patch \
        python-dev \
        python-setuptools \
        zlib1g-dev &&\
        apt-get -y clean
