#!/usr/bin/env bash
# Start nginx

/etc/init.d/nginx start

# Activate Stack, setup dax_webserv, and run uwsgi
su webserv -c'\
source /lsst/stack/loadLSST.bash; \
setup dax_webserv; \
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib; \
uwsgi --master --processes 40 --threads 1 \
    --socket /tmp/webserv.sock \
    --buffer-size 32768 \
    --wsgi-file $DAX_WEBSERV_DIR/bin/imgserver.py --callable app'
