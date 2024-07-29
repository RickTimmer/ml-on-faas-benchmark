import json
import logging
import uuid
import os
from datetime import datetime
from config import functionName

logger = logging.getLogger()
logger.setLevel(logging.INFO)

is_cold_start = True
function_instance_id = str(uuid.uuid4())

lambda_info = {
    "AWS_LAMBDA_FUNCTION_NAME": os.environ.get("AWS_LAMBDA_FUNCTION_NAME"),
    "AWS_LAMBDA_FUNCTION_MEMORY_SIZE": os.environ.get("AWS_LAMBDA_FUNCTION_MEMORY_SIZE"),
    "AWS_LAMBDA_FUNCTION_VERSION": os.environ.get("AWS_LAMBDA_FUNCTION_VERSION")
}

cpu_count = os.cpu_count()

experiment_id = ""
message_id = ""
lambda_request_id = ""
batch_size = 0

# Define a custom formatter
class CustomFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')
        record.msg = 'ML_ON_FAAS - {{"timeStamp": "{}", "functionName": "{}", "functionInstanceId": "{}", "experimentId": "{}", "messageId": "{}", "batchSize": "{}", "isColdStart": "{}", "lambdaRequestId": "{}", "lambdaName": "{}", "lambdaMemorySize": "{}", "lambdaVersion": "{}", "cpuCount": "{}", "logMessage": "{}"}}'.format(
          timestamp, 
          functionName, function_instance_id, experiment_id, message_id, batch_size, is_cold_start,
          lambda_request_id, lambda_info["AWS_LAMBDA_FUNCTION_NAME"], lambda_info["AWS_LAMBDA_FUNCTION_MEMORY_SIZE"], lambda_info["AWS_LAMBDA_FUNCTION_VERSION"],
          cpu_count,
          record.msg
        )
        return super().format(record)

def wrap(event, callback, initializer, requestId):
  body = json.loads(event['Records'][0]['Sns']['Message'])
  batch = body.get("Batch", [])

  global lambda_request_id, batch_size, is_cold_start, experiment_id, message_id
  lambda_request_id = requestId
  batch_size = len(batch)
  experiment_id = body.get("ExperimentId", "NO_EXPERIMENT_ID")
  message_id = body.get("MessageId", "NO_MESSAGE_ID")

  # Configure custom logger if it is the first run of the instance.
  if is_cold_start:
     configureLogger()
     logger.info("Initialization started")
     initializer()
     logger.info("Initialization completed")
     
  logger.info(f"Processing started")
  results = callback(batch)
  logger.info("Processing completed")

  # When the first run of the instance has completed it is no longer cold.
  if is_cold_start:
     is_cold_start = False

  return {
      'statusCode': 200,
      'batch': json.dumps(results)
  }

def configureLogger():
  handler = logging.StreamHandler()
  formatter = CustomFormatter()
  handler.setFormatter(formatter)
  logger.addHandler(handler)
