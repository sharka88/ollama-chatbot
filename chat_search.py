import streamlit as st
import ollama
from langchain_community.chat_models import ChatOllama
from langchain_community.agents import initialize_agent, AgentType
from langchain_community.callbacks import StreamlitCallbackHandler
#from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

# Function to generate Ollama response
def gen_ollama_response(prompt_input):
    response = ollama.chat(
        model=st.session_state.selected_model,
        messages=[{'role': 'user', 'content': prompt_input}],
    )
    if 'message' in response and 'content' in response['message']:
        return response['message']['content']
    else:
        return "Error: Unexpected response format from the model."
    
with st.sidebar:
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

st.title("🔎 Chat with search")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle new user input
if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Generate Ollama response
    response = gen_ollama_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

    # Initialize the search tool
    search = DuckDuckGoSearchRun(name="Search")

    # Initialize the agent with the search tool and Ollama response
    #llm = ChatOllama(model="mistral", temperature=0)
    llm = ChatOllama(model=str(selected_model), temperature=0)
    search_agent = initialize_agent(
        [search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True
    )
    # Get and display the search agent's response
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response_from_search = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        full_response = response + "\n\n" + response_from_search
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.write(full_response)
