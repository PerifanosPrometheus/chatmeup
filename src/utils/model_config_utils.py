import json
import streamlit as st

# from langchain_community.llms import LlamaCpp
from src.utils.prompt_preparation import generate_prompt_template

import os

# Make sure you created an environment variable containing the package directory. 
# Look at README.md for more information
#Define module directory
PACKAGE_DIR = os.environ.get('MODULE_PATH')

class Model_Constructor:
    def __init__(self, model_type):
        self.model_type = model_type
        self.model_config_file = os.path.join(PACKAGE_DIR, 'model_config/'+model_type+'-config.json')
        self.load_config()

    def load_config(self):
        # Load model configuration from file
        with open(self.model_config_file, 'r') as f:
             self.config = json.load(f)
        self.model_path = self.config.pop("model_path")
        self.model_template = self.config.pop("model_template")
        self.prompt=generate_prompt_template(self.model_type)
        pass