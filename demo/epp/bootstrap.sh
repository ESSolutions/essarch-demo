#!/bin/bash

start_time=`date +%s`

set -e

mkdir -p /ESSArch/log/ \
         /ESSArch/data/gate/reception \
         /ESSArch/data/epp/ingest \
         /ESSArch/data/epp/cache \
         /ESSArch/data/epp/work \
         /ESSArch/data/epp/disseminations \
         /ESSArch/data/epp/orders \
         /ESSArch/data/epp/verify \
         /ESSArch/data/epp/temp \
         /ESSArch/data/epp/reports/appraisal \
         /ESSArch/data/epp/reports/conversion

ln -fs /usr/bin/python3.6 /usr/bin/python
python -m pip install --upgrade pip setuptools
python -m pip install -e ${EC}/["tests,s3,postgres,logstash"]
cd ${EPP}/frontend/static/frontend && yarn && gulp

set +e

end_time=`date +%s`
runtime=$((end_time-start_time))

echo "
Bootstrap took ${runtime} seconds!
"
