import docker
import os
import logging
import yaml
import time

def build_project(project_dir, reg_user, reg_pass, detached, metrics, metrics_enabled):
    
    build_metrics = {}
    start_time = 0
    
    # Check if the project directory is valid
    if not os.path.exists(f"{project_dir}/gen"):
        logging.error(f"Project directory is not valid")
        return
    
    print('Building WASM components')
    
    os.environ["DOCKER_CLIENT_TIMEOUT"] = "120"
    os.environ["DOCKER_TIMEOUT"] = "120"
    
    # Docker client
    client = docker.from_env()
    
    if metrics_enabled:
        start_time = time.time()
    
    # Build the images for the project if they don't exist
    try:
        client.images.get("wash-build-image:latest")
    except docker.errors.ImageNotFound:
        
        print(' - Building wash-build-image from Dockerfile...')
        client.images.build(
            path="src/wasm_builder/docker",
            dockerfile="build.Dockerfile",
            tag="wash-build-image:latest"
        )
        if metrics_enabled:
            build_metrics['image_build_time'] = '%.3f'%(time.time() - start_time)
        
    try:
        wait_list = []
        
        for task in os.listdir(f"{project_dir}/gen"):
            __build_wasm(f"{project_dir}/gen/{task}", client, reg_user, reg_pass, detached, wait_list)
            
        if detached == 'True':
            
            print('Waiting for build to finish...')
            for container in wait_list:
                try:
                    client.containers.get(container).wait()
                except Exception:
                    continue
        
    except Exception as e:
        logging.error(f"Error building project: {e}")
        return
    
    if metrics_enabled:
        build_metrics['components_build_time'] = '%.3f'%(time.time() - start_time)
        metrics['build'] = build_metrics
        
    print("Project built successfully")
    
def __build_wasm(task_dir, client, reg_user, reg_pass, detached, wait_list):
    
    wadm = __parse_yaml(f"{task_dir}/wadm.yaml")
    
    path = os.path.abspath(task_dir)
    
    oci_url = wadm['spec']['components'][0]['properties']['image']
    name = wadm['spec']['components'][0]['name'] + '-build'
    
    uid = os.getuid()
    gid = os.getgid()
    
    # Build the wasm module
    print(f" - Building WASM module {oci_url}")
    container = client.containers.run(
        "wash-build-image:latest",
        environment=[f'REGISTRY={oci_url}',
                     f'WASH_REG_USER={reg_user}',
                     f'WASH_REG_PASSWORD={reg_pass}',
                     f'HOST_UID={uid}',
                     f'HOST_GID={gid}'],
        volumes={path: {'bind': '/app', 'mode': 'rw'}},
        remove=True,
        detach=True,
        name=name
    )
    
    if detached == 'False':
        container.wait()
    else:
        wait_list.append(name)
    

def __parse_yaml(yaml_file):
    with open(yaml_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None