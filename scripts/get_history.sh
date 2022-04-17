#!/bin/bash

cd "$(find $HOME -name 'slow-trade-machine')"
source venv/bin/activate
python src/upload_data.py