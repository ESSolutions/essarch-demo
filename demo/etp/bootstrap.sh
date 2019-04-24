#!/bin/bash

start_time=`date +%s`

set -e

mkdir -p /ESSArch/log/ \
         /ESSArch/etp/env \
         /ESSArch/data/etp/prepare \
         /ESSArch/data/etp/prepare_reception \
         /ESSArch/data/eta/reception/eft

ln -fs /usr/bin/python3.6 /usr/bin/python
python -m pip install --upgrade pip
python -m pip install -e ${EC}/["tests,s3,postgres,mysql,logstash"]
cd ${ETP}/frontend/static/frontend && yarn && gulp

set +e

end_time=`date +%s`
runtime=$((end_time-start_time))

echo "
Bootstrap took ${runtime} seconds!
"