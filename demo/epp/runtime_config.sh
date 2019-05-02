#!/bin/bash

while ! nc -z logstash 9600; do echo "waiting for logstash..."; sleep 3; done
while ! nc -z $ELASTICSEARCH_HOST $ELASTICSEARCH_PORT; do echo "waiting for elasticsearch..."; sleep 3; done
while ! nc -z $DB_HOST $DB_PORT; do echo "waiting for database..."; sleep 3; done

start_time=`date +%s`

set -e

python ESSArch_PP/manage.py migrate
python ${EC}/ESSArch_Core/install/install_default_config.py
python ESSArch_PP/install/install_default_config_epp.py
python ESSArch_PP/install/install_profiles_epp_se.py

set +e

end_time=`date +%s`
runtime=$((end_time-start_time))

echo "
Configure took ${runtime} seconds!
"
