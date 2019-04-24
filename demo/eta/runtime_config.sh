#!/bin/bash

start_time=`date +%s`

set -e

python ESSArch_TA/manage.py migrate
python ${EC}/ESSArch_Core/install/install_default_config.py
python ESSArch_TA/install/install_default_config_eta.py

set +e

end_time=`date +%s`
runtime=$((end_time-start_time))

echo "
Configure took ${runtime} seconds!
"
