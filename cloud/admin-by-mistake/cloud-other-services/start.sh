#!/bin/bash

redis-server --dir /tmp --requirepass R3d1sP@ssw0rd! --daemonize yes
sleep 1
redis-cli -a R3d1sP@ssw0rd! set vault_secret_key "sunshine_is_not_enough_123"

python3 generate_db.py

python3 metadata_app.py &
python3 apache_app.py &
python3 vault_app.py &
python3 log_store_app.py &
python3 k8s_app.py &
python3 analytics_app.py &
python3 user_db_app.py &
python3 archive_app.py &

wait
