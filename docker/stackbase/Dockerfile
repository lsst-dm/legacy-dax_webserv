# Have this follow the latest stack image.
FROM lsstsqre/centos:7-stack-lsst_distrib-latest
MAINTAINER Christine Banek <cbanek@lsst.org>

USER root

# Configure nginx
COPY etc/nginx/nginx.conf /etc/nginx/nginx.conf
COPY etc/nginx/sites-enabled/webserv /etc/nginx/sites-enabled/webserv

# Bring in ENTRYPOINT
COPY webserv/entrypoint.sh /webserv/entrypoint.sh

# Switch to root so we can start nginx,
# entrypoint does a `su webserv` internally to start wsgi as
# as webserv
ENTRYPOINT /webserv/entrypoint.sh

# Install packages and run additional commands.
COPY bake.sh /root/bake.sh
RUN /root/bake.sh
