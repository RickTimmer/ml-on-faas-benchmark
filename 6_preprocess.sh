#!/bin/bash

# Source the .env file
if [ -f .env ]; then
    source .env
    export $(grep -v '^#' .env | xargs)
fi

# Get the first argument, if empty get the last alphabetical directory name in data/unprocessed
if [ -z "$1" ]; then
    DIRECTORY=$(ls -1 data/unprocessed | sort -r | head -n 1)
else
    DIRECTORY=$1
    if [ ! -d "data/unprocessed/$DIRECTORY" ]; then
        echo "Directory $DIRECTORY does not exist."
        exit 1
    fi
fi

# Rest of your code
python scripts/preprocess.py "data/unprocessed/$DIRECTORY"
# python scripts/check_message_counts.py
# python analyse/plot.py
