#!/bin/bash -ex
source /opt/lsst/software/stack/loadLSST.bash

cd ~
git clone https://github.com/lsst/dax_dbserv.git
git clone https://github.com/lsst/dax_metaserv.git
git clone https://github.com/lsst/dax_imgserv.git
git clone https://github.com/lsst/dax_webserv.git
git clone https://github.com/lsst/dax_webservcommon.git -b tickets/DM-15396

(cd dax_webservcommon && python setup.py install)
