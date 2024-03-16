import os

PACKAGE_DIR = os.environ.get('MODULE_PATH')
MODEL_CONFIG_DIR = os.path.join(PACKAGE_DIR, '/model_config')
MODEL_DIR = os.path.join(PACKAGE_DIR, '/models')
PROMPT_TEMPLATE_DIR = os.path.join(PACKAGE_DIR, '/prompt_templates')
SRC_DIR = os.path.join(PACKAGE_DIR, '/src')
MAIN_DIR = os.path.join(PACKAGE_DIR, '/src/main')
UTILS_DIR = os.path.join(PACKAGE_DIR, '/src/utils')

LOGO_PATH = os.path.join(PACKAGE_DIR, '/src/main/streamlit/logo.png')