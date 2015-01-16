# Useful link:
http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

# To install flask:
sudo aptitude install python-flask

# To run some quick tests:

  # clone metaserv
  git clone git@git.lsstcorp.org:LSST/DMS/metaserv.git metaserv

  # load the metaserv schema and load some dummy data
  ./reinit.sh

  # run the server
  python server.py

  # and fetch the urls:
  http://localhost:5000/meta
  http://localhost:5000/meta/v0
  http://localhost:5000/meta/v0/db
  http://localhost:5000/meta/v0/db/L3
  http://localhost:5000/meta/v0/db/L3/jacek_db1x
  http://localhost:5000/meta/v0/db/L3/jacek_db1x/tables
  http://localhost:5000/meta/v0/db/L3/jacek_db1x/tables/Object
  http://localhost:5000/meta/v0/db/L3/jacek_db1x/tables/Source/schema
