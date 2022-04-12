#!/bin/bash

cd "$(find $HOME -name 'slow-trade-machine')"
export PYTHONPATH=$PYTHONPATH:$PWD/src
source venv/bin/activate
python3 src/auth/reset_refresh_token.py