#!/bin/bash -ex
# We need this to get mysql_config, which is required to
# install the mysqlclient python package which dbserv
# depends on.
yum install -y mysql-devel nginx

chown -R lsst:lsst /webserv
chown -R lsst:lsst /var/lib/nginx

source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib

cd ~
git clone https://github.com/lsst/dax_webservcommon.git -b master
(cd dax_webservcommon && pip install -r requirements.txt && pip install . && python setup.py test)

git clone https://github.com/lsst/dax_metaserv.git -b master
(cd dax_metaserv && pip install -r requirements.txt && pip install . && python setup.py test)

git clone https://github.com/lsst/dax_dbserv.git -b master
(cd dax_dbserv && pip install -r requirements.txt && pip install . && python setup.py test)

git clone https://github.com/lsst/dax_imgserv.git -b master
# TODO(DM-15694): Still need to fix imgserv test.
#(cd dax_imgserv && pip install -r requirements.txt && pip install . && python setup.py test)
(cd dax_imgserv && pip install -r requirements.txt && pip install .)

pip install uwsgi
git clone https://github.com/lsst/dax_webserv.git
