from langchain.prompts import PromptTemplate
import os

# Make sure you created an environment variable containing the package directory. 
# Look at README.md for more information
#Define module directory
PACKAGE_DIR = os.environ.get('MODULE_PATH')

def generate_prompt(prompt_template_file_name, input):
    input = input.strip()
    with open(os.path.join(PACKAGE_DIR, 'prompt_templates/inference/'+prompt_template_file_name+'.txt'), 'r') as f:
        s = f.read()
    return s.format(input=input)


def generate_prompt_template(prompt_template_file_name):
    with open(os.path.join(PACKAGE_DIR, 'prompt_templates/inference/'+prompt_template_file_name+'.txt'), 'r') as f:
        template = f.read()
    langchain_template = PromptTemplate(template=template, input_variables=["input"])
    return langchain_template
