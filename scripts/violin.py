import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from config import results_dir

# Read data
df = pd.read_csv(f'{results_dir}/results.csv')
df = df[df['isColdStart'] == False]
df = df[df['lambdaMemorySize'] != 4096]
df = df[df['lambdaMemorySize'] != 6144]
df = df[df['lambdaMemorySize'] != 8192]
df = df[df['lambdaMemorySize'] != 10240]

plt.figure(figsize=(5, 5))  # Adjust the width (first value) as needed

violin_plot = sns.violinplot(x="lambdaMemorySize", y="lambdaBilledDuration", data=df, alpha=[0.3, 0.6, 0.4, 0.2], width=0.9)
violin_plot.set_ylabel('Billed Duration (ms)')
violin_plot.set_xlabel('Memory Size (MB)')

plt.savefig(f'{results_dir}/violin_plot.png')
