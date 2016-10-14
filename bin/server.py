#!/usr/bin/env python

# LSST Data Management System
# Copyright 2015 AURA/LSST.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.

"""
This is RESTful LSST Data Access Web Server. It handles /meta, /image, and /db

@author  Jacek Becla, SLAC
"""

from flask import Flask, request
import json
import logging as log
import os
import sys

from lsst.dax.dbserv import dbREST_v0
from lsst.dax.imgserv import imageREST_v0
from lsst.dax.metaserv import metaREST_v0
from lsst.db.engineFactory import getEngineFromFile

try:
    from ConfigParser import RawConfigParser, NoSectionError
except ImportError:
    from configparser import RawConfigParser, NoSectionError

log.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S',
    level=log.DEBUG)

defaults_file = os.environ.get("CONFIG_FILE", "~/.lsst/dbAuth-dbServ.ini")

engine = getEngineFromFile(defaults_file)

app = Flask(__name__)

parser = RawConfigParser()

with open(os.path.expanduser(defaults_file)) as cfg:
    parser.readfp(cfg, defaults_file)

app.config["default_engine"] = engine
app.config["dax.imgserv.default_source"] = "/lsst7/releaseW13EP"

# Execute this last, we can overwrite anything we don't like
app.config.update(dict(parser.items("webserv")))


@app.route('/')
def route_webserv_root():
    fmt = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    if fmt == 'text/html':
        return ("LSST Web Service here. I currently support: "
                "<a href='meta'>/meta</a>, "
                "<a href='image'>/image</a>, "
                "<a href='db'>/db</a.")
    return "LSST Web Service here. I currently support: /meta, /image, /db."


@app.route('/db')
def route_dbserv():
    """Lists supported versions for /db."""
    fmt = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    if fmt == 'text/html':
        return "<a href='db/v0'>v0</a>"
    return json.dumps("v0")


@app.route('/image')
def route_imgserv():
    """Lists supported versions for /image."""
    fmt = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    if fmt == 'text/html':
        return "<a href='image/v0'>v0</a>"
    return json.dumps("v0")


@app.route('/meta')
def route_metaserv():
    """Lists supported versions for /meta."""
    fmt = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    if fmt == 'text/html':
        return "<a href='meta/v0'>v0</a>"
    return json.dumps("v0")

app.register_blueprint(dbREST_v0.dbREST, url_prefix='/db/v0')
app.register_blueprint(imageREST_v0.imageREST, url_prefix='/image/v0')
app.register_blueprint(metaREST_v0.metaREST, url_prefix='/meta/v0')

if __name__ == '__main__':
    log.basicConfig(
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S',
        level=log.DEBUG)

    try:
        app.run(debug=True)
    except Exception, e:
        print "Problem starting the server.", str(e)
        sys.exit(1)
