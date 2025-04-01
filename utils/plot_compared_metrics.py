import seaborn as sns
import matplotlib.pyplot as plt
import yaml
import pandas as pd
import numpy as np
import os

# Function to read and parse a metric file
def read_metrics(file_path, label):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    runs = data['runs']
    
    extracted_data = []
    for run in runs:
        if 'build' in run:
            extracted_data.append({'Task': run['n_task'], 'Type': 'Build Time', 'Time': float(run['build']['components_build_time']), 'Source': label})

        if 'code_gen' in run:
            extracted_data.append({'Task': run['n_task'], 'Type': 'Generation Time', 'Time': float(run['code_gen']['gen_time']), 'Source': label})

        if 'deploy' in run:
            extracted_data.append({'Task': run['n_task'], 'Type': 'Deployment Time', 'Time': float(run['deploy']['components_deploy_time']), 'Source': label})

        if 'time_total' in run:
            extracted_data.append({'Task': run['n_task'], 'Type': 'Total Time', 'Time': float(run['time_total']), 'Source': label})

    return extracted_data

# Paths for the two metric files
file_path_1 = 'res/metrics/metrics-parallel-nats.yaml'  # First metrics file
file_path_2 = 'res/metrics/metrics-sequential.yaml'  # Second metrics file

# Read and combine the data
data1 = read_metrics(file_path_1, 'Esecuzione Parallelizzata')
data2 = read_metrics(file_path_2, 'Esecuzione Sequenziale')

df = pd.DataFrame(data1 + data2)

# Ensure benchmark directory exists
os.makedirs('benchmark', exist_ok=True)

# Function to plot boxplot
def plot_boxplot(metric, filename):
    subset = df[df['Type'] == metric]
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Task', y='Time', hue='Source', data=subset, showfliers=False)

    plt.ylabel('Time (seconds)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Source')
    plt.tight_layout()
    plt.savefig(f'benchmark/{filename}')
    plt.close()

# Function to plot line plot with confidence intervals
def plot_lineplot(metric, filename):
    subset = df[df['Type'] == metric]
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Task', y='Time', hue='Source', data=subset, errorbar=('ci', 95), linewidth=2, marker='o')

    plt.xlabel('Number of Tasks')
    plt.ylabel('Time (seconds)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Source')
    plt.tight_layout()
    plt.savefig(f'benchmark/{filename}')
    plt.close()

# Function to plot bar plot with confidence intervals
def plot_barplot(metric, filename):
    subset = df[df['Type'] == metric]
    plt.figure(figsize=(10, 6))
    
    sns.barplot(x='Task', y='Time', hue='Source', data=subset, errorbar=('ci', 95), palette=['salmon', 'skyblue'])

    plt.xlabel('Task', fontsize=14)  # Aumenta la dimensione del font dell'asse X
    plt.ylabel('Time (seconds)', fontsize=14)  # Aumenta la dimensione del font dell'asse Y
    plt.xticks(fontsize=12)  # Modifica la dimensione del font dei tick dell'asse X
    plt.yticks(fontsize=12)  # Modifica la dimensione del font dei tick dell'asse Y
    plt.legend(title='Source', title_fontsize=14, fontsize=12)  # Modifica il font della legenda

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'benchmark/{filename}')
    plt.close()


# Generate plots for each metric
metrics = ['Build Time', 'Generation Time', 'Deployment Time', 'Total Time']
filenames = ['build_time', 'gen_time', 'deploy_time', 'total_time']

for metric, filename in zip(metrics, filenames):
    #plot_boxplot(metric, f'{filename}_boxplot.png')
    #plot_lineplot(metric, f'{filename}_lineplot.png')
    plot_barplot(metric, f'{filename}_paired_barplot.png')

print('Comparison plots saved successfully in "benchmark" directory!')
