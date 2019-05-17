#!/bin/bash

start_time=`date +%s`

set -e

ln -fs /usr/bin/python3.6 /usr/bin/python
python -m pip install --upgrade pip setuptools
python -m pip install -e ${EC}/["tests,s3,postgres,logstash"]
cd ${ETA}/frontend/static/frontend && yarn && gulp

set +e

end_time=`date +%s`
runtime=$((end_time-start_time))

echo "
Bootstrap took ${runtime} seconds!
"
