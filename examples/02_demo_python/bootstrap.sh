#!/bin/bash

# Enable VirtualEnv with the following command:
# $ source ./bootstrap.sh


venv=${1:-virtualenv}

## setup virtualenv if not already exist
if [[ ! -e ${venv} ]]; then
  virtualenv --python=python ${venv}
  ${venv}/bin/pip install pip -r requirements.txt

fi

## start virtualenv
source ${venv}/bin/activate





