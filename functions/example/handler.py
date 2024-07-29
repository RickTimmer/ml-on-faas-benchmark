import time
import random
import wrapper

def lambda_handler(event, context):
  requestId = context.aws_request_id
  return wrapper.wrap(event, handler, initializer, requestId)

def handler(batch):
  results = []
  for item in batch:
    time.sleep(random.randint(1, 5) / 1000) # Mock processing time.
    results.append(item)
  return results

def initializer():
  # Initialize model on cold start.
  return
