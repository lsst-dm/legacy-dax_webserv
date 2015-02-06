#!/usr/bin/python

# todo: need to properly package Flask
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
Hello, World, this is a very first version of LSST Web Data Access. Try:<br />
/meta/v%d<br />
/db/v%d</br />
/image/v%d
""" % (curVerMeta, curVerDb, curVerImg)


# /meta is handled through metaserv/server.py
# /db   is handled through ???
# image is handled through imgserv/server.py

if __name__ == '__main__':
    app.run(debug=True)
