import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from config import results_dir

# Read data
df = pd.read_csv(f'{results_dir}/results.csv')
df = df[df['isColdStart'] == False]

# Create box plot
box_plot = sns.boxplot(
    x="lambdaMemorySize", 
    y="lambdaBilledDuration",
    hue="lambdaMemorySize",
    legend=False,
    data=df,
    palette="Set2"
)

plt.savefig(f'{results_dir}/box_plot.png')
