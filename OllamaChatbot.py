import streamlit as st
from langchain_community.llms import Ollama
#import os

# App title
st.set_page_config(page_title="🦙 Ollama Chatbot 💬 ")

# Sidebar for Replicate Credentials
with st.sidebar:
    st.title('🦙 Ollama Chatbot 💬')

    # Model selection and parameters
    st.subheader('Models and parameters')
    model_list = ollama.list()['models']
    model_names = [model['model'] for model in model_list]

    # If session_state does not have selected_model, set default model
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = model_names[0]  # Default to the first model

    # Create a dropdown menu using session_state to track selection
    selected_model = st.selectbox("Select a model", model_names, index=model_names.index(st.session_state.selected_model))
    st.session_state.selected_model = selected_model  # Update selected model

    # Parameters for the LLM
    temperature = st.slider('Temperature', min_value=0.01, max_value=5.0, value=0.5, step=0.01)
    top_p = st.slider('Top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('Max Length', min_value=64, max_value=4096, value=512, step=8)

    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

# Initialize chat messages in session_state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "有什麼我可以幫上忙的嗎?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Clear chat history function
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def gen_ollama_response(prompt_input):
    response = ollama.chat(model=st.session_state.selected_model, messages=[{'role': 'user', 'content': prompt_input}])
    #st.write("Debug: Response from ollama.chat:", response)  # Debug print
    if 'message' in response and 'content' in response['message']:
        return response['message']['content']
    else:
        return "Error: Unexpected response format from the model."

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = gen_ollama_response(st.session_state.messages[-1]["content"])
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
