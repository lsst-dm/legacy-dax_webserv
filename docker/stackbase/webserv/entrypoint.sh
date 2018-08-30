#!/usr/bin/env bash
# Start nginx
nginx

# Activacte Stack, setup dax_webserv, and run
# uwsgi under the lsst UID.
source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib
uwsgi --master --processes 40 --threads 1 \
    --socket /tmp/webserv.sock --uid lsst \
    --callable app --need-app \
    --wsgi-file /root/dax_webserv/bin/server.py
