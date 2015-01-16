#!/usr/bin/python

# todo: need to properly package Flask
from flask import Flask
import MySQLdb

app = Flask(__name__)

# connect to database metaServ
# todo: this will currently fail if metaServ db does not exist
# todo: db connection and credentials need to be handled better
dbHost = "localhost"
dbPort = 3306
dbUser="becla"
dbPass = ""
dbName = "metaServ"
con = MySQLdb.connect(host=dbHost, 
                      port=dbPort,
                      user=dbUser,
                      passwd=dbPass,
                      db=dbName)
cursor = con.cursor()

@app.route('/')
def index():
    return """
Hello, World, this is a very first version of LSST Web Data Access. Try:<br />
/meta/v%d<br />
/db/v%d</br />
/image/v%d
""" % (curVerMeta, curVerDb, curVerImg)

##### This handles /meta API #######################################################

curVerMeta = 0 # version of the API for /meta

# Print list of supported versions for /meta
@app.route('/meta', methods=['GET'])
def get_meta():
    return "v%d" % curVerMeta

@app.route('/meta/v%d' % curVerMeta, methods=['GET'])
def get_meta_curVer():
    return "image<br />db"

@app.route('/meta/v%d/image' % curVerMeta, methods=['GET'])
def get_meta_curVer_image():
    return ("meta/.../image not implemented. I am supposed to print list of " 
            "supported image types here, something like: raw, template, coadd, "
            "jpeg, calexp, ... etc")

@app.route('/meta/v%d/db' % curVerMeta, methods=['GET'])
def get_meta_curVer_db():
    # todo: this will currently fail if Repo table does not exist
    cursor.execute("SELECT lsstLevel, shortName FROM Repo WHERE repoType = 'db'")
    ret = cursor.fetchall()
    if len(ret) == 0:
        return("No database found.")
    str = '''<table border='1'>
  <tr><td>Level</td><td>Db name</td></tr>
'''
    for r in ret:
        str += '''  <tr><td>%s</td><td>%s</td></tr>
''' % (r[0], r[1])
    str += "</table>"
    return str

##### This handles /db API #########################################################

curVerDb = 0 # version of the API for /db

# Print list of supported versions for /db
@app.route('/db', methods=['GET'])
def get_db():
    return "v%d" % curVerDb

@app.route('/db/v%d' % curVerDb, methods=['GET'])
def get_db_curVer():
    return "The db section is not implemented yet"

##### This handles /image ##########################################################

curVerImg = 0 # version of the API for /image

# Print list of supported versions for /db
@app.route('/image', methods=['GET'])
def get_image():
    return "v%d" % curVerImg

@app.route('/image/v%d' % curVerImg, methods=['GET'])
def get_image_curVer():
    return "The image section is not implemented yet"

##### Main #########################################################################
if __name__ == '__main__':
    app.run(debug=True)
