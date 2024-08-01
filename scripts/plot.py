import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from config import results_dir

# Read data
df = pd.read_csv(f'{results_dir}/results.csv')

# Remove cold start
df_hot = df[df['isColdStart'] == False]
df_cold = df[df['isColdStart'] == True]

def create_plot(isColdStart, dataframe):
    # Get unique lambdaNames
    unique_lambdas = dataframe['functionName'].unique()

    # Create subplots
    num_cols = len(unique_lambdas)
    fig, axes = plt.subplots(nrows=1, ncols=num_cols, figsize=(7*num_cols, 6), squeeze=False)

    for i, lambda_name in enumerate(unique_lambdas):
        lambda_df = dataframe[dataframe['functionName'] == lambda_name]
        sns.boxplot(data=lambda_df, x='lambdaMemorySize', y='lambdaBilledDuration', ax=axes[0, i])

        axes[0, i].set_title(lambda_name)
        axes[0, i].set_xlabel('Memory Size (MB)')
        if i == 0:
            axes[0, i].set_ylabel('Billed Duration (milliseconds)')
        else:
            axes[0, i].set_ylabel('')

    plt.tight_layout()
    plt.savefig(f'{results_dir}/violin_isCold_{isColdStart}.png')

create_plot(False, df_hot)
create_plot(True, df_cold)
