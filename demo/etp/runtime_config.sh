#!/bin/bash

start_time=`date +%s`

set -e

python ESSArch_TP/manage.py migrate
python ${EC}/ESSArch_Core/install/install_default_config.py
python ESSArch_TP/install/install_default_config_etp.py

set +e

end_time=`date +%s`
runtime=$((end_time-start_time))

echo "
Configure took ${runtime} seconds!
"
