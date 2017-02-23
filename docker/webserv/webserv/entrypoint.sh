#!/usr/bin/env bash
# Start nginx

/etc/init.d/nginx start

# Activacte Stack, setup dax_webserv, and run uwsgi
su webserv <<EOF
source /lsst/stack/loadLSST.bash
setup dax_webserv
uwsgi --master --processes 40 --threads 1 \
    --socket /tmp/webserv.sock \
    --wsgi-file $DAX_WEBSERV_DIR/bin/server.py --callable app 2> /webserv/log.txt
EOF
