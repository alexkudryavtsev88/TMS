#!/bin/bash


# Copy the PATH to the your ROOT folder (where all this code is placed) and set this PATH
# instead of my path!
YOUR_ROOT_PATH=/home/a2kudryavtsev/tms/students/1_aliaksei_kudrautsau/TMS

export PYTHONPATH=${YOUR_ROOT_PATH}

python ${YOUR_ROOT_PATH}/lesson21_client_server_database/client_and_server/server.py
