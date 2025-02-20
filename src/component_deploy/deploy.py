import docker
import os
import logging
import yaml
import time

def deploy_components(project_dir, nats_host, nats_port, detached, metrics, metrics_enabled):

    deploy_metrics = {}
    
    # Check if the project directory is valid
    if not os.path.exists(f"{project_dir}/gen"):
        logging.error(f"Project directory is not valid")
        return
    
    print('Deploying WASM components')
    
    # Docker client
    client = docker.from_env()
    
    if metrics_enabled:
        start_time = time.time()
    
    # Build the images for the project if they don't exist
    try:
        client.images.get("wash-deploy-image:latest")
    except:
        
        print(' - Building wash-deploy-image from Dockerfile...')
        client.images.build(
            path="src/component_deploy/docker",
            dockerfile="deploy.Dockerfile",
            tag="wash-deploy-image:latest"
        )
        if metrics_enabled:
            deploy_metrics['image_build_time'] = '%.3f'%(time.time() - start_time)
        
    try:
        wait_list = []
        
        for task in os.listdir(f"{project_dir}/gen"):
            __deploy_wadm(f"{project_dir}/gen/{task}", client, nats_host, nats_port, detached, wait_list)
            
        if detached == 'True':
            
            print('Waiting for deployment...')
            for container in wait_list:
                try:
                    client.containers.get(container).wait()
                except Exception:
                    continue
        
    except Exception as e:
        logging.error(f"Error deploying project: {e}")
        return
    
    if metrics_enabled:
        deploy_metrics['components_deploy_time'] = '%.3f'%(time.time() - start_time)
        metrics['deploy'] = deploy_metrics
        
    print("Project deployed successfully")
    
def __deploy_wadm(task_dir, client, nats_host, nats_port, detached, wait_list):
    
    wadm = __parse_yaml(f"{task_dir}/wadm.yaml")
    
    path = os.path.abspath(task_dir)
    
    name = wadm['spec']['components'][0]['name'] + '-deploy'
    
    # Build the wasm module
    print(f" - Deploying WASM module {name}")
    container = client.containers.run(
        "wash-deploy-image:latest",
        environment=[f'WASMCLOUD_CTL_HOST={nats_host}',
                     f'WASMCLOUD_CTL_PORT={nats_port}'],
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