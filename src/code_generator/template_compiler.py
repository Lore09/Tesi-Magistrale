import logging
from jinja2 import FileSystemLoader, Environment
import os
import shutil

def handle_task(task, output_dir):
    
    try:
    
        match task['type']:
            case 'http_producer_nats':
                __generate_producer(task, output_dir)
            case 'processor_nats':
                __generate_processor(task, output_dir)
            case 'dbsync_nats':
                __generate_dbsync(task, output_dir)
            case _:
                logging.error(f"Task type {task['type']} not supported")
                pass
    except KeyError as e:
        logging.error(f"Error parsing task: {e}")
        pass
    
def __generate_producer(task, output_dir):
    
    # Copy the template folder to the output folder
    __copytree("src/code_generator/templates/producer_nats", f"{output_dir}/{task['component_name']}")
    
    # Replace each file of the output dir with the template
    for filename in os.listdir(f"{output_dir}/{task['component_name']}"):
        
        # Skip the following files
        if filename in ['Dockerfile', 'go.mod', 'go.sum', 'tools.go']:
            continue
        
        # Skip if it's a directory
        if os.path.isdir(f"{output_dir}/{task['component_name']}/{filename}"):
            continue
        
        __replace_file_with_template(filename, f"{output_dir}/{task['component_name']}", task)
    

def __generate_processor(task, output_dir):
    # Copy the template folder to the output folder
    __copytree("src/code_generator/templates/processor_nats", f"{output_dir}/{task['component_name']}")
    
    # Replace each file of the output dir with the template
    for filename in os.listdir(f"{output_dir}/{task['component_name']}"):
        
        # Skip the following files
        if filename in ['Dockerfile', 'go.mod', 'go.sum', 'tools.go', 'bindings.wadge.go']:
            continue
        
        # Skip if it's a directory
        if os.path.isdir(f"{output_dir}/{task['component_name']}/{filename}"):
            continue
        
        __replace_file_with_template(filename, f"{output_dir}/{task['component_name']}", task)

def __generate_dbsync(task, output_dir):
    pass

def __copytree(src, dst, symlinks=False, ignore=None):
    
    # Create the destination directory
    os.makedirs(dst, exist_ok=True)
    
    # Copy the files
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
            
def __replace_file_with_template(filename, output_dir, template_vars):
    
    try: 
        templateLoader = FileSystemLoader(searchpath=output_dir)
        templateEnv = Environment(loader=templateLoader)
        template = templateEnv.get_template(filename)
        
        outputText = template.render(template_vars)
        
        # Replace the file with the rendered template
        with open(f"{output_dir}/{filename}", 'w') as f:
            f.write(outputText)
        
    except Exception as e:
        logging.error(f"Error rendering template {filename}: {e}")
        return