#!/bin/bash

# Source the .env file
if [ -f .env ]; then
    source .env
fi

source ./.last_run

# Timestamp in START (unix in ms) to format 2024-05-15_19:04
START_TIMESTAMP=$(date -d @$((START/1000)) +"%Y-%m-%d_%H:%M")

RESULT_DIR="data/unprocessed/$START_TIMESTAMP"

echo "Retrieving logs..."

LOG_GROUP_NAME="ml-on-faas-experiments-log-group"
LOG_STREAM_NAME=$(aws logs describe-log-streams --log-group-name $LOG_GROUP_NAME --order-by LastEventTime --descending --query 'logStreams[0].logStreamName' --output text)
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Fetch the logs from the log stream
EXPERIMENT_LOGS=$(aws logs get-log-events --log-group-name $LOG_GROUP_NAME --log-stream-name $LOG_STREAM_NAME --query 'events[].message' --output text)
EXPERIMENT_LOGS_WITH_NEWLINES=$(echo "$EXPERIMENT_LOGS" | sed 's/\[Experiments\]/\n\[Experiments\]/g')

# Store experiment logs
mkdir -p "$RESULT_DIR"
echo "$EXPERIMENT_LOGS_WITH_NEWLINES" > "$RESULT_DIR/experiments_container.log"

# Split image tags and memory sizes into arrays
IFS=',' read -ra IMAGE_TAGS <<< "$TF_VAR_image_tags"
IFS=',' read -ra MEMORY_SIZES <<< "$TF_VAR_memory_sizes"

# Loop over image tags and memory sizes to create log groups
for image_tag in "${IMAGE_TAGS[@]}"; do
  for memory_size in "${MEMORY_SIZES[@]}"; do
    LOG_GROUP="/aws/lambda/ml-on-faas-${image_tag}-${memory_size}MB"
    FUNCTION_LOGS=$(aws logs filter-log-events --log-group-name "$LOG_GROUP" --start-time $START --query 'events[].message' --output text)

    FUNCTION_NAME=$(basename $LOG_GROUP)

    # Remove tab characters at the beginning of each line
    FUNCTION_LOGS=$(echo "$FUNCTION_LOGS" | sed 's/^\t//g')

    echo "$FUNCTION_LOGS" > "$RESULT_DIR/${FUNCTION_NAME}.log"
  done
done

echo "Logs retrieved..."