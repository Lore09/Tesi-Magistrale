from dotenv import load_dotenv
import os

import src.code_generator.generator as code_generator

class Pelato:
    def __init__(self):
        
        self.setup_vars()
        
    def setup_vars(self):
        load_dotenv()
        
        self.registry_url = os.getenv('REGISTRY_URL')
        self.reg_user = os.getenv('REGISTRY_USER')
        self.reg_pass = os.getenv('REGISTRY_PASSWORD')
        
    def generate(self, project_dir):
        print(f"Generating Go code for project {project_dir}")
        code_generator.generate(project_dir)
        
    def build(self, project_dir):
        print(f"Building WASM component for project {project_dir}")
        
    def deploy(self, project_dir):
        print(f"Deploying WASM components for project {project_dir}")
        
    def all(self, project_dir):
        print(f"Doing everything for project {project_dir}")