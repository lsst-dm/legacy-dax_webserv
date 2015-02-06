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

from flask import Flask
from lsst.metaserv import metaREST_v0
from lsst.imgserv import imageREST_v0
#TODO dbREST

app = Flask(__name__)

@app.route('/')
def index():
    return '''LSST Web Service here. I currently support: /meta, /image.
'''

app.register_blueprint(metaREST_v0.metaREST, url_prefix='/meta')
app.register_blueprint(imageREST_v0.imageREST, url_prefix='/image')

if __name__ == '__main__':
    app.run(debug=True)
