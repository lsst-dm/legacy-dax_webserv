#!/bin/sh

# Start the server
echo "Starting the Authorizer..."
export UWSGI_THREADS=10
export UWSGI_PROCESSES=2
export UWSGI_OFFLOAD_THREADS=10
export UWSGI_MODULE=authorizer:app

# Have gzipped versions ready for direct serving by uwsgi

uwsgi --ini /app/uwsgi.ini --pyargv "-c /etc/authorizer.cfg" &
echo "uWSGI Authorizer started: $auth_pid"
nginx -g "daemon off;"
