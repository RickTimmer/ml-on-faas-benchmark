#!/bin/bash

# Usage: ./script_name.sh [-r aws_region] [-i ecr_repository_id] [dir1 dir2 dir3 ...]
# Default AWS Region and ECR Repository ID are set below.

# Source the .env file
if [ -f .env ]; then
    source .env
    export $(grep -v '^#' .env | xargs)
fi

AWS_REGION=$TF_VAR_aws_region
ECR_ID=$TF_VAR_ecr_id

# Parse command line options
while getopts ":r:i:" opt; do
  case $opt in
    r) AWS_REGION=$OPTARG ;;
    i) ECR_ID=$OPTARG ;;
    \?) echo "Invalid option -$OPTARG" >&2; exit 1 ;;
  esac
done
shift $((OPTIND -1))

# Login to AWS ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build experiments image
docker build -t ml-on-faas:experiments experiments
docker tag ml-on-faas:experiments $ECR_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ml-on-faas:experiments
docker push $ECR_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ml-on-faas:experiments

# Switch to functions
FUNCTIONS_DIR="./functions"
cd "$FUNCTIONS_DIR"

# Build base image which contains the wrapper
docker build . -t ml-on-faas:base

# Process directories
if [ $# -eq 0 ]; then
  # If no directories specified, process all directories
  set -- */  # Set positional parameters to all directories
fi
IFS=',' read -ra IMAGE_TAGS <<< "$TF_VAR_image_tags"
for dir in "$@"; do
  if [ -d "$dir" ]; then
    dir_name="${dir%/}"  # Remove trailing slash if present

    # Only build images that are specified in the .env file
    if [[ ! " ${IMAGE_TAGS[@]} " =~ " $dir_name " ]]; then
      echo "Skipping $dir_name since it's not specified in the .env"
      continue
    fi

    (
      docker build -t ml-on-faas:$dir_name $dir &&
      docker tag ml-on-faas:$dir_name $ECR_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ml-on-faas:$dir_name &&
      docker push $ECR_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ml-on-faas:$dir_name
    ) &  # Run the command in background
  fi
done

# Wait for all background processes to finish
wait