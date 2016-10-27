FROM webserv/webserv:base
MAINTAINER Brian Van Klaveren <bvan@slac.stanford.edu>

ARG LSST_STACK_DIR=/lsst/stack
ARG INSTALL_MINICONDA=Y
ARG LSST_USER=webserv
ARG LSST_GROUP=webserv
ARG LSST_WORKSPACE=/webserv
ARG EUPS_PRODUCT=dax_webserv
ARG EUPS_TAG=12.1

RUN groupadd $LSST_GROUP
RUN useradd -m -g $LSST_USER $LSST_GROUP
RUN usermod -s /bin/bash $LSST_USER

# Make sure $LSST_STACK_DIR and $LSST_WORKSPACE have proper permissions
RUN mkdir -p $LSST_STACK_DIR && chown $LSST_USER:$LSST_GROUP $LSST_STACK_DIR
RUN mkdir -p $LSST_WORKSPACE && chown $LSST_USER:$LSST_GROUP $LSST_WORKSPACE

# Install the stack as $LSST_USER
USER $LSST_USER
WORKDIR $LSST_STACK_DIR

RUN curl -OL https://raw.githubusercontent.com/lsst/lsst/12.1/scripts/newinstall.sh && \
    echo $INSTALL_MINICONDA | bash newinstall.sh && \
    cd $LSST_WORKSPACE && \
    /bin/bash -c 'source $LSST_STACK_DIR/loadLSST.bash; eups distrib install -t $EUPS_TAG $EUPS_PRODUCT'
