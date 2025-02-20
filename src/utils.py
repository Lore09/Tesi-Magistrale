import yaml
import os

def dump_metrics(metrics, project_dir):
    
    with open(f"{project_dir}/metrics.yaml", 'w') as file:
        yaml.dump(metrics, file)
    
    print(f"Metrics saved in {project_dir}metrics.yaml")
    
    return

def load_metrics(project_dir):
    
    if not os.path.exists(f"{project_dir}/metrics.yaml"):
        return {
            "runs": []
        }
    
    with open(f"{project_dir}/metrics.yaml", 'r') as file:
        metrics = yaml.safe_load(file)
    
    return metrics