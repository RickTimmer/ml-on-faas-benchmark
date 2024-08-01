import os

data_dir = "data"
last_dir = sorted(os.listdir(data_dir))[-1]
results_dir = os.path.join(data_dir, last_dir)
