FROM lsstsqre/centos:7-stack-lsst_distrib-w_2018_33
MAINTAINER Christine Banek <cbanek@lsst.org>

COPY bake.sh /home/lsst/bake.sh
RUN /home/lsst/bake.sh

# Bring in ENTRYPOINT
COPY webserv/entrypoint.sh /webserv/entrypoint.sh

# Switch to root so we can start nginx,
# entrypoint does a `su webserv` internally to start wsgi as
# as webserv
ENTRYPOINT /webserv/entrypoint.sh
