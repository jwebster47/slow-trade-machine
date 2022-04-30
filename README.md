# Run the relevant commands at the top level of the repository:


### Setup script to install required packages and create virtual environment

    bash scripts/setup.sh

### Add project source to shell profile

    export PYTHONPATH=$PYTHONPATH:$PWD/src

### Activate virtual environment

    source venv/bin/activate


# This project uses python to pull equity price history, load it to an S3 bucket, make price forecasts, and execute trades based on a defined strategy
