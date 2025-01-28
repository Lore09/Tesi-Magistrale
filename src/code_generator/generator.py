import yaml
import shutil
import logging
import os
import src.code_generator.template_compiler as template_compiler

def __parse_yaml(yaml_file):
    with open(yaml_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None
        
def __remove_dir_if_exists(dir_path):
    
    if os.path.exists(dir_path):
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)

def generate(project_dir):
    
    # Parsing del file di configurazione
    config = __parse_yaml(f"{project_dir}/workflow.yaml")
    
    if config is None:
        logging.error("Error parsing workflow.yaml")
        return
    
    # Rimozione della cartella di output
    output_dir = f"{project_dir}/gen"
    __remove_dir_if_exists(output_dir)
    
    # Creazione della cartella di output
    os.makedirs(output_dir, exist_ok=True)
    
    # for each task in the workflow
    for task in config['tasks']:
        template_compiler.handle_task(task, output_dir)
    