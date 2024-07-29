#!/bin/bash

# Source the .env file
if [ -f .env ]; then
    source .env
    export $(grep -v '^#' .env | xargs)
fi

# Retrieve networking identifiers
cd ./artifacts
security_group_id=$(terraform output default_security_group_id)

# Turn the subnet_ids into a correctly formatted string
subnet_ids=$(terraform output default_subnet_ids)
subnet_ids=$(echo "$subnet_ids" | tr -d '[:space:]') # Remove whitespaces
subnet_ids=${subnet_ids#"tolist(["} # Remove leading 'tolist(['
subnet_ids=${subnet_ids%"])"} # Remove trailing '"])'
subnet_ids=${subnet_ids//\"/} # Remove double quotes
subnet_ids=${subnet_ids//\", \"/,} # Remove double quotes and comma
subnet_ids=$(echo "$subnet_ids" | sed 's/,$//') # Remove trailing comma
cd ..

START=$(date +%s%N | cut -b1-13)

# Store somewhere so another script can use the START later
echo "START=$START" > .last_run

# # Execute the experiment task
echo "Starting ECS task..."
task_id=$(aws ecs run-task --cluster ml-on-faas-cluster \
  --task-definition ml-on-faas-cluster-experiments-task \
  --network-configuration "awsvpcConfiguration={subnets=[$subnet_ids],securityGroups=[$security_group_id],assignPublicIp=\"ENABLED\"}" \
  --query 'tasks[0].taskArn' --output text)

if [ $? -eq 0 ]; then
  echo "ECS task started successfully."
  echo "Task ID: $task_id"
else
  echo "Failed to start ECS task. Exiting..."
  exit 1
fi

# Wait until the task is finished
echo "Waiting for the ECS task to finish..."
aws ecs wait tasks-stopped --cluster ml-on-faas-cluster --tasks $task_id
echo "ECS task finished."
