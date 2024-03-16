##Import packages and functions
import streamlit as st
import base64
import sys
import os

# Make sure you created an environment variable containing the package directory. 
# Look at README.md for more information
#Define module and logo directories
PACKAGE_DIR = os.environ.get('MODULE_PATH')
sys.path.append(PACKAGE_DIR)

from src.utils.model_config_utils import Model_Constructor
from langchain.chains import LLMChain
from langchain_community.llms import LlamaCpp


LOGO_IMAGE = os.path.join(PACKAGE_DIR, 'src/main/streamlit/logo/logo.png')

#Define page title and add logo
st.markdown(
    f"""
    <div style="text-align: center;">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
    </div>
    """,
    unsafe_allow_html=True
)

# Provide some fun text to describe what the application does
st.markdown(
    f"""
    <div style="text-align: center;">
        <p>
        Hello My Friend!
        </p>
        <p class="logo-text">
        &#x1F44B; Hello! Hola! Ciao!\n Use me to test your custom models &#x1F603;
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Add a selectbox to the sidebar:
model_type=st.sidebar.selectbox(
                'Model',
                ('llama-2-13b-chat','codellama-7b')
            )

# Add a selectbox to sidebar. This will be used to determine if user wants to use quantized model or not
max_tokens = st.sidebar.slider(
                'Max Tokens To Generate',
                min_value=100,
                max_value=4096,
                value=1000
            )

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

#clear chat history
def clear_chat_history():
    st.session_state.mode = 'generate'
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

#initialize model cinstructor class
llm_constructor = Model_Constructor(model_type)

#define function to load the model for inference
@st.cache_resource
def load_model(model_path, config, **kwargs):
    '''Load model based on model_path.
    Model_path should point to the *.gguf file for the model.'''
    llm = LlamaCpp(
            model_path=model_path,
            n_gpu_layers=config["n_gpu_layers"],
            n_ctx=config["n_ctx"],
            n_threads=config["n_threads"],
            max_tokens=kwargs["max_tokens"],
            rope_freq_base=config["rope_freq_base"],
            temperature=config["temperature"],
            top_p=config["top_p"],
            echo=False,
            stop=['</s>'],
            verbose=True,
            streaming=False,
        )
    return llm

#load co model
llm = load_model(llm_constructor.model_path,llm_constructor.config,max_tokens=max_tokens)

#create chain
chain = LLMChain(llm=llm, prompt=llm_constructor.prompt)

# Function for generating llm response
def generate_llm_response(model_input):
    output = chain.invoke(model_input)
    return output

# User-provided prompt
if model_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": model_input})
    with st.chat_message("user"):
        st.write(model_input)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llm_response(model_input)['text']
            placeholder = st.empty()
            full_response=response
            placeholder.write(response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)