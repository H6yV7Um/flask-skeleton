#!/usr/bin/env bash
source $(dirname "$0")/env.sh

# create virtual env
virtualenv $PROJECT_ROOT_PATH/deploy/venv
source $PROJECT_ROOT_PATH/deploy/venv/bin/activate
pip install -r $PROJECT_ROOT_PATH/requirements.txt


# start supervisord
$PROJECT_ROOT_PATH/deploy/venv/bin/supervisord -c $PROJECT_ROOT_PATH/deploy/supervisor/supervisord.conf
$PROJECT_ROOT_PATH/deploy/venv/bin/supervisorctl -c $PROJECT_ROOT_PATH/deploy/supervisor/supervisord.conf update
