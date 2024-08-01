import sys
import re
import os
import datetime

# Get the first parameter
results_dir = sys.argv[1]

with open(f"{results_dir}/experiments_container.log", "r") as f:
    f.readline() # Omit first line
    line = f.readline()
    pattern = r"experiment:\s+(\S+)"
    experiment_id = re.search(pattern, line).group(1)

log_files = os.listdir(results_dir)
log_files.remove("experiments_container.log")

messages = {}
            
def extract_messages(lines):
    for line in lines:
        if "ML_ON_FAAS - " in line:
            if "Received event" in line:
                continue
            lambdaRequestId = re.search(r"lambdaRequestId\":\s+\"(\S+)\"", line).group(1)
            if lambdaRequestId not in messages:
                functionName = re.search(r"functionName\":\s+\"(\S+)\"", line).group(1)
                functionInstanceId = re.search(r"functionInstanceId\":\s+\"(\S+)\"", line).group(1)
                batchSize = re.search(r"batchSize\":\s+(\S+)", line).group(1).replace(",", "")
                isColdStart = re.search(r"isColdStart\":\s+(\S+)", line).group(1).replace(",", "")
                messageId = re.search(r"messageId\":\s+\"(\S+)\"", line).group(1)
                lambdaName = re.search(r"lambdaName\":\s+\"(\S+)\"", line).group(1)
                cpuCount = re.search(r"cpuCount\":\s+\"(\S+)\"", line).group(1) if "cpuCount" in line else "NA"
                messages[lambdaRequestId] = {
                    "messageId": messageId,
                    "functionInstanceId": functionInstanceId,
                    "functionName": functionName,
                    "lambdaRequestId": lambdaRequestId,
                    "lambdaName": lambdaName,
                    "batchSize": batchSize,
                    "isColdStart": isColdStart,
                    "cpuCount": cpuCount,
                    "processingStart": "NA",
                    "processingEnd": "NA",
                    "processingTime": "NA",
                    "initializationStart": "NA",
                    "initializationEnd": "NA",
                    "initializationTime": "NA",
                    "lambdaDuration": "NA",
                    "lambdaBilledDuration": "NA",
                    "lambdaMemorySize": "NA",
                    "lambdaMaxMemoryUsed": "NA"
                }

            timestamp = re.search(r'"timeStamp": "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)"', line).group(1)
            
            if "Initialization started" in line:
                messages[lambdaRequestId]["initializationStart"] = timestamp
            elif "Initialization completed" in line:
                messages[lambdaRequestId]["initializationEnd"] = timestamp
            elif "Processing started" in line:
                messages[lambdaRequestId]["processingStart"] = timestamp
            elif "Processing completed" in line:
                messages[lambdaRequestId]["processingEnd"] = timestamp

        if "REPORT RequestId: " in line:
            lambdaRequestId = re.search(r"RequestId:\s+(\S+)", line).group(1)
            messages[lambdaRequestId]["lambdaDuration"] = re.search(r"Duration:\s+(\S+)", line).group(1)
            messages[lambdaRequestId]["lambdaBilledDuration"] = re.search(r"Billed Duration:\s+(\S+)", line).group(1)
            messages[lambdaRequestId]["lambdaMemorySize"] = re.search(r"Memory Size:\s+(\S+)", line).group(1)
            messages[lambdaRequestId]["lambdaMaxMemoryUsed"] = re.search(r"Max Memory Used:\s+(\S+)", line).group(1)
for log_file in log_files:
  if not log_file.endswith(".log"):
    continue
  if log_file.startswith("_"):
    continue
  with open(f"{results_dir}/{log_file}", "r") as f:
    lines = f.readlines()
    extract_messages(lines)

for key in messages:
  

    if "initializationStart" in messages[key] and "initializationEnd" in messages[key] and messages[key]["initializationStart"] != "NA" and messages[key]["initializationEnd"] != "NA":
        diffInMs = datetime.datetime.strptime(messages[key]["initializationEnd"], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(messages[key]["initializationStart"], "%Y-%m-%d %H:%M:%S.%f")
        diffInMs = int(diffInMs.total_seconds() * 1000)
        messages[key]["initializationTime"] = diffInMs


    if "processingStart" in messages[key] and "processingEnd" in messages[key] and messages[key]["processingStart"] != "NA" and messages[key]["processingEnd"] != "NA":
        diffInMs = datetime.datetime.strptime(messages[key]["processingEnd"], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(messages[key]["processingStart"], "%Y-%m-%d %H:%M:%S.%f")
        diffInMs = int(diffInMs.total_seconds() * 1000)
        messages[key]["processingTime"] = diffInMs

experiment_name = input("Enter the name for the experiment: ")
with open(f"data/processed/{experiment_name} ({experiment_id}).csv", "w") as f:
    f.write("messageId,lambdaName,functionName,functionInstanceId,batchSize,isColdStart,initializationStart,initializationEnd,processingStart,processingEnd,initializationTime,processingTime,lambdaDuration,lambdaBilledDuration,lambdaMemorySize,lambdaMaxMemoryUsed,cpuCount\n")
    for key in messages:
        f.write(f"{messages[key]['messageId']},{messages[key]['lambdaName']},{messages[key]['functionName']},{messages[key]['functionInstanceId']},{messages[key]['batchSize']},{messages[key]['isColdStart']},{messages[key]['initializationStart']},{messages[key]['initializationEnd']},{messages[key]['processingStart']},{messages[key]['processingEnd']},{messages[key]['initializationTime']},{messages[key]['processingTime']},{messages[key]['lambdaDuration']},{messages[key]['lambdaBilledDuration']},{messages[key]['lambdaMemorySize']},{messages[key]['lambdaMaxMemoryUsed']},{messages[key]['cpuCount']}\n")
