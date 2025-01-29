import docker
import os
import logging
import yaml

def build_project(project_dir, reg_user, reg_pass, detached):
    
    # Check if the project directory is valid
    if not os.path.exists(f"{project_dir}/gen"):
        logging.error(f"Project directory is not valid")
        return
    
    # Docker client
    client = docker.from_env()
    
    # Build the images for the project if they don't exist
    try:
        client.images.get("wash-build-image:latest")
    except docker.errors.ImageNotFound:
        client.images.build(
            path="src/wasm_builder/docker",
            dockerfile="build.Dockerfile",
            tag="wash-build-image:latest"
        )
        
    try:
        for task in os.listdir(f"{project_dir}/gen"):
            __build_wasm(f"{project_dir}/gen/{task}", client, reg_user, reg_pass, detached)
    except Exception as e:
        logging.error(f"Error building project: {e}")
        return
    
    print("Project built successfully")
    
def __build_wasm(task_dir, client, reg_user, reg_pass, detached):
    
    wadm = __parse_yaml(f"{task_dir}/wadm.yaml")
    
    path = os.path.abspath(task_dir)
    
    oci_url = wadm['spec']['components'][0]['properties']['image']
    
    # Build the wasm module
    print(f" - Building WASM module {oci_url}")
    container = client.containers.run(
        "wash-build-image:latest",
        environment=[f'REGISTRY={oci_url}',
                     f'WASH_REG_USER={reg_user}',
                     f'WASH_REG_PASSWORD={reg_pass}'],
        volumes={path: {'bind': '/app', 'mode': 'rw'}},
        remove=True,
        detach=True
    )
    
    if detached == 'False':
        container.wait()
    

def __parse_yaml(yaml_file):
    with open(yaml_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None