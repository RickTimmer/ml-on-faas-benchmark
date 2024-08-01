import csv
from config import results_dir

# Read CSV with format messageId,lambdaName,functionName,functionInstanceId,batchSize,isColdStart,initializationTime,processingTime,lambdaDuration,lambdaBilledDuration,lambdaMemorySize,lambdaMaxMemoryUsed
with open(f"{results_dir}/results.csv", "r") as f:
  # Count the number of rows for each lambdaName
  reader = csv.DictReader(f)
  counts = {}
  billableTimes = {}
  for row in reader:
    counts[row["lambdaName"]] = counts.get(row["lambdaName"], 0) + 1
  # Print the counts for each name
  for name, count in counts.items():
    print(f"Message counts for {name}: {count}")
  