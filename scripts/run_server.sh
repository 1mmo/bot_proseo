#!/bin/bash

VENV=./venv
DEPLOY_FLAG=/opt/proseo/deploy_state.flag

touch $DEPLOY_FLAG

if [ ! -d $VENV ]; then
    `which python3` -m venv $VENV
    $VENV/bin/pip install -U pip
fi

$VENV/bin/pip install -r requirements.txt

$VENV/bin/python src/manage.py migrate
$VENV/bin/python src/manage.py collectstatic

$VENV/bin/python src/manage.py runserver 0.0.0.0:8000

rm -f $DEPLOY_FLAG

echo "Run Django"
