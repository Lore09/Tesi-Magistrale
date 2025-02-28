import seaborn as sns
import matplotlib.pyplot as plt
import yaml
import pandas as pd

# Function to read and parse the file
def read_metrics(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data['runs']

# Read metrics from the file
file_path = 'project/metrics.yaml'  # Replace with your file path
runs = read_metrics(file_path)

#Flatten data into a list of dictionaries
data = []
for run in runs:
    if 'build' in run:
        data.append({'Task': run['n_task'], 'Type': 'Build Time', 'Time': float(run['build']['components_build_time'])})

    if 'code_gen' in run:
        data.append({'Task': run['n_task'], 'Type': 'Generation Time', 'Time': float(run['code_gen']['gen_time'])})
    
    if 'deploy' in run:
        data.append({'Task': run['n_task'], 'Type': 'Deployment Time', 'Time': float(run['deploy']['components_deploy_time'])})

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to plot and add median labels
def plot_metric(metric, filename, color):
    subset = df[df['Type'] == metric]
    plt.figure(figsize=(8, 6))
    ax = sns.boxplot(x='Task', y='Time', data=subset, color=color)

    # Add median labels
    medians = subset.groupby('Task')['Time'].median()
    for i, task in enumerate(medians.index):
        median_value = medians[task]
        ax.text(i, median_value, f'{median_value:.3f}', ha='center', va='center',
                fontsize=10, color='white', bbox=dict(facecolor='black', alpha=0.6, boxstyle='round,pad=0.3'))

    plt.title(f'{metric} by Number of Tasks')
    plt.xlabel('Number of Tasks')
    plt.ylabel('Time (seconds)')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# Plot each metric separately
plot_metric('Build Time', 'res/build_time_boxplot.png', 'skyblue')
plot_metric('Generation Time', 'res/gen_time_boxplot.png', 'lightgreen')
plot_metric('Deployment Time', 'res/deploy_time_boxplot.png', 'salmon')

print('Plots saved successfully!')