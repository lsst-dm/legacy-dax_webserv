FROM webserv/webserv:base
MAINTAINER Brian Van Klaveren <bvan@slac.stanford.edu>

ARG LSST_STACK_DIR=/lsst/stack
ARG EUPS_HOME=$LSST_STACK_DIR/.eups
ARG EUPS_PRODUCT=dax_webserv
ARG EUPS_TAG=dax_latest
ARG EUPS_PRODUCT_VERSION=
ARG INSTALL_MINICONDA=Y

ARG LSST_USER=webserv
ARG LSST_GROUP=webserv
ARG LSST_WORKSPACE=/webserv

RUN mkdir -p $LSST_STACK_DIR
RUN mkdir -p $EUPS_HOME
RUN mkdir -p $LSST_WORKSPACE

WORKDIR $LSST_STACK_DIR

RUN echo "Environment: \n" && env | sort

RUN groupadd $LSST_GROUP
RUN useradd -m -g $LSST_USER $LSST_GROUP
RUN usermod -s /bin/bash $LSST_USER

RUN chown -R $LSST_USER:$LSST_GROUP $LSST_STACK_DIR

# Install stack as $LSST_USER - this is really expensive to fix permissions on
USER $LSST_USER

# If $EUPS_TAG exists, prepend with a "-t"
RUN echo "Executing: eups distrib install ${EUPS_TAG:+"-t"} $EUPS_TAG $EUPS_PRODUCT $EUPS_PRODUCT_VERSION" && \
    curl -OL https://raw.githubusercontent.com/lsst/lsst/master/scripts/newinstall.sh && \
        echo $INSTALL_MINICONDA | bash newinstall.sh && \
        /bin/bash -c 'source $LSST_STACK_DIR/loadLSST.bash; \
            eups distrib install ${EUPS_TAG:+"-t"} $EUPS_TAG $EUPS_PRODUCT $EUPS_PRODUCT_VERSION;'

USER root

# Webserv parts...
# Setup nginx
RUN apt-get update && apt-get --yes install nginx
COPY etc/nginx/nginx.conf /etc/nginx/nginx.conf
COPY etc/nginx/sites-enabled/webserv /etc/nginx/sites-enabled/webserv

# Setup uwsgi. Note that Ubuntu uwsgi seems to have issues
# This is a hack. This will install uwsgi in Miniconda's
# site-packages
RUN /bin/bash -c 'source $LSST_STACK_DIR/loadLSST.bash; \
    pip install uwsgi'

# Bring in ENTRYPOINT
COPY webserv/entrypoint.sh /webserv/entrypoint.sh

# Fix permissions again :(
RUN chown -R $LSST_USER:$LSST_GROUP $LSST_WORKSPACE

# Switch to root so we can start nginx,
# entrypoint does a `su webserv` internally to start wsgi as
# as webserv
ENTRYPOINT /webserv/entrypoint.sh
