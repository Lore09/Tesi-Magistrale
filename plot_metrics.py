import matplotlib.pyplot as plt
import yaml

# Function to read and parse the file
def read_metrics(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data['runs']

# Read metrics from the file
file_path = 'project/metrics.yaml'  # Replace with the correct file path
runs = read_metrics(file_path)

# Extracting values
n_tasks = [run['n_task'] for run in runs]
build_times = [float(run['build']['components_build_time']) for run in runs]
gen_times = [float(run['code_gen']['gen_time']) for run in runs]
deploy_times = [float(run['deploy']['components_deploy_time']) for run in runs]

# Plotting Build Time
plt.figure(figsize=(8, 6))
ax = plt.gca()  # Get current axis
p = ax.bar(n_tasks, build_times, color='b')
ax.bar_label(p, label_type='edge')
ax.set_title('Build Time')
ax.set_xlabel('Number of Tasks')
ax.set_ylabel('Build Time (seconds)')
plt.tight_layout()
plt.savefig('build_time_plot.png')  # Save the plot as an image
plt.close()

# Plotting Code Generation Time
plt.figure(figsize=(8, 6))
ax = plt.gca()  # Get current axis
p = ax.bar(n_tasks, gen_times, color='g')
ax.bar_label(p, label_type='edge')
ax.set_title('Code Generation Time')
ax.set_xlabel('Number of Tasks')
ax.set_ylabel('Generation Time (seconds)')
plt.tight_layout()
plt.savefig('gen_time_plot.png')  # Save the plot as an image
plt.close()

# Plotting Deployment Time
plt.figure(figsize=(8, 6))
ax = plt.gca()  # Get current axis
p = ax.bar(n_tasks, deploy_times, color='r')
ax.bar_label(p, label_type='edge')
ax.set_title('Deployment Time')
ax.set_xlabel('Number of Tasks')
ax.set_ylabel('Deployment Time (seconds)')
plt.tight_layout()
plt.savefig('deploy_time_plot.png')  # Save the plot as an image
plt.close()