from dotenv import load_dotenv
import os

class Pelato:
    def __init__(self, project_dir):
        
        self.project_dir = project_dir
        
        self.setup_vars()
        
    def setup_vars(self):
        load_dotenv()
        
        self.registry_url = os.getenv('REGISTRY_URL')
        self.reg_user = os.getenv('REGISTRY_USER')
        self.reg_pass = os.getenv('REGISTRY_PASSWORD')
        
    def generate(self):
        print(f"Generating Go code for project {self.project_dir}")
        
    def build(self):
        print(f"Building WASM component for project {self.project_dir}")
        
    def deploy(self):
        print(f"Deploying WASM components for project {self.project_dir}")
        
    def all(self):
        print(f"Doing everything for project {self.project_dir}")