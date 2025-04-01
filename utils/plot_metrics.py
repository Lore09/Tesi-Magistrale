import seaborn as sns
import matplotlib.pyplot as plt
import yaml
import pandas as pd
import numpy as np
import os

# Function to read and parse the file
def read_metrics(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data['runs']

# Read metrics from the file
file_path = 'res/metrics-parallel.yaml'  # Replace with your file path
runs = read_metrics(file_path)

# Flatten data into a list of dictionaries
data = []
for run in runs:
    if 'build' in run:
        data.append({'Task': run['n_task'], 'Type': 'Build Time', 'Time': float(run['build']['components_build_time'])})

    if 'code_gen' in run:
        data.append({'Task': run['n_task'], 'Type': 'Generation Time', 'Time': float(run['code_gen']['gen_time'])})

    if 'deploy' in run:
        data.append({'Task': run['n_task'], 'Type': 'Deployment Time', 'Time': float(run['deploy']['components_deploy_time'])})
    
    if 'time_total' in run:
        data.append({'Task': run['n_task'], 'Type': 'Total Time', 'Time': float(run['time_total'])})

# Convert to DataFrame
df = pd.DataFrame(data)

# Make sure the benchmark directory exists
os.makedirs('benchmark', exist_ok=True)

# Function to plot boxplot
def plot_boxplot(metric, filename, color):
    subset = df[df['Type'] == metric]
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Task', y='Time', data=subset, color=color, showfliers=False)

    # Label median values
    medians = subset.groupby('Task')['Time'].median()
    for i, task in enumerate(medians.index):
        median_value = medians[task]
        plt.text(i, median_value, f'{median_value:.3f}', ha='center', va='center', fontsize=10, color='white',
                 bbox=dict(facecolor='black', alpha=0.6, boxstyle='round,pad=0.3'))

    plt.ylabel('Time (seconds)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'benchmark/{filename}')
    plt.close()

# Function to plot line plot with confidence intervals
def plot_lineplot(metric, filename, color):
    subset = df[df['Type'] == metric]
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Task', y='Time', data=subset, errorbar=('ci', 95), color=color, linewidth=2, marker='o')

    min_task = subset['Task'].min()
    max_task = subset['Task'].max()
    all_tasks = np.arange(min_task, max_task + 1)
    plt.xticks(all_tasks)

    for i, row in subset.groupby('Task')['Time'].median().reset_index().iterrows():
        plt.text(row['Task'], row['Time'], f'{row["Time"]:.3f}', ha='center', va='bottom', fontsize=10)

    plt.xlabel('Number of Tasks')
    plt.ylabel('Time (seconds)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'benchmark/{filename}')
    plt.close()

# Function to plot bar plot with confidence intervals
def plot_barplot(metric, filename, color):
    subset = df[df['Type'] == metric]
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Task', y='Time', data=subset, color=color, errorbar=('ci', 95))

    means = subset.groupby('Task')['Time'].mean()
    for i, task in enumerate(means.index):
        mean_value = means[task]
        plt.text(i, 0, f'{mean_value:.3f}', ha='center', va='bottom', fontsize=10, alpha=0.7)

    plt.ylabel('Time (seconds)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'benchmark/{filename}')
    plt.close()

# Plot each metric separately
#plot_boxplot('Build Time', 'build_time_boxplot.png', 'skyblue')
#plot_lineplot('Build Time', 'build_time_lineplot.png', 'skyblue')
plot_barplot('Build Time', 'build_time_barplot.png', 'skyblue')

#plot_boxplot('Generation Time', 'gen_time_boxplot.png', 'lightgreen')
#plot_lineplot('Generation Time', 'gen_time_lineplot.png', 'lightgreen')
plot_barplot('Generation Time', 'gen_time_barplot.png', 'lightgreen')

#plot_boxplot('Deployment Time', 'deploy_time_boxplot.png', 'salmon')
#plot_lineplot('Deployment Time', 'deploy_time_lineplot.png', 'salmon')
plot_barplot('Deployment Time', 'deploy_time_barplot.png', 'salmon')

#plot_boxplot('Total Time', 'total_time_boxplot.png', 'purple')
#plot_lineplot('Total Time', 'total_time_lineplot.png', 'purple')
plot_barplot('Total Time', 'total_time_barplot.png', 'orange')

print('Plots saved successfully in "benchmark" directory!')
