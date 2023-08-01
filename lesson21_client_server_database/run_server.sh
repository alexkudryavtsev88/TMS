#!/bin/bash


# Copy the PATH to your ROOT folder (where all this code is placed) and set this PATH
# instead of my path!
ROOT_PATH=${PWD}
echo ${ROOT_PATH}

export PYTHONPATH=${ROOT_PATH}/..

python ${PWD}/client_and_server/server.py
