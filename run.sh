#!/bin/bash

#BASEDIR=$(dirname "$0")
#PY_VENV=$BASEDIR/venv/bin
#$PY_VENV/python3 $BASEDIR/timestamp.py $1
#------------------------------------------

#export WORKSPACE=`pwd`
#export PYTHONWARNINGS="ignore:Unverified HTTPS request"

# Setup
VENV_DIR=.venv
if [[ ! (-f "$VENV_DIR" && -f "$VENV_DIR/bin/activate" && -f "$VENV_DIR/bin/python3") ]]; then
  python3 -m pip install --user --upgrade virtualenv
  python3 -m virtualenv $VENV_DIR
fi

if [[ -f "$VENV_DIR/bin/activate" && -f "$VENV_DIR/bin/python3" ]]; then
  source ./$VENV_DIR/bin/activate
  if [[ ! $(pip3 list | grep moviepy) ]]; then
    pip3 install moviepy
  fi
else
    echo "Python virtual env 'venv' doesn't exist. Create corretly or just remove current 'venv' virtual environment in this folder."
    exit
fi

# Run
python3 timestamp.py $1 $2







