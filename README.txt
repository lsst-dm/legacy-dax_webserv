# Useful link:
http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

# To install flask:
sudo aptitude install python-flask

# To run some quick tests:
  # clone metaserv
  git clone git@git.lsstcorp.org:LSST/DMS/metaserv.git metaserv
  # load the metaserv schema
  cd metaserv/sql
  mysql -e "drop database metaServ; create database metaServ"
  mysql metaServ < global.sql
  mysql metaServ < dbRepo.sql
  mysql metaServ < fileRepo.sql
  # load some dummy data
  mysql metaServ -e "INSERT INTO Repo(url, project, repoType, lsstLevel, shortName, owner) VALUES
     ('/u1/mysql_data/AlertProd',          'LSST', 'db',   'L1', 'AlertProd',     1),
     ('/u1/mysql_data/W13_stripe82',       'LSST', 'db',   'L2', 'W13_stripe82',  1),
     ('/u1/mysql_data/S13_stripe82',       'LSST', 'db',   'L2', 'S13_stripe82',  1),
     ('/u1/mysql_data/jacek_db1',          'LSST', 'db',   'L3', 'jacek_db1',     2),
     ('/u1/mysql_data/john_tmpDb5',        'LSST', 'db',   'L3', 'john_tmpDb5',   3),
     ('/u1/images/external/SDSS/Stripe82', 'SDSS', 'file', 'L2', 'SDSS_stripe82', 1),
     ('/u1/images/lsst/raw',               'LSST', 'file', 'L1', 'raw',           1),
     ('/u1/images/lsst/coadds',            'LSST', 'file', 'L2', 'coadds',        1) "


 # run the server
 python server.py

 # and fetch the urls:
  http://localhost:5000/meta/
  http://localhost:5000/meta/v0
  http://localhost:5000/meta/v0/db
  and so on...
