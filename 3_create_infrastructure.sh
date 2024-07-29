#!/bin/bash

# Source the .env file
if [ -f .env ]; then
    source .env
    export $(grep -v '^#' .env | xargs)
fi

# Change working directory
cd artifacts

terraform apply
