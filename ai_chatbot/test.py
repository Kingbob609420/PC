import streamlit as st
import duckdb
import requests
import json
import re
from datetime import datetime

# App configuration
st.set_page_config(page_title="🐳💬 Local Ollama Chatbot", initial_sidebar_state="expanded")

# Initialize DuckDB connection
conn = duckdb.connect(':memory:')

# Ollama configuration
OLLAMA_URL = ("http://localhost:1684/api/generate")  # Default Ollama API endpoint
MODEL_NAME = "llama3.1"  # Default model, change to 'mistral', 'phi3', etc.

# Model parameters configuration
MODEL_PARAMS = {
    'temperature': {'min': 0.01, 'max': 1.0, 'default': 0.7, 'step': 0.01},
    'top_p': {'min': 0.01, 'max': 1.0, 'default': 1.0, 'step': 0.01},
    'max_tokens': {'min': 10, 'max': 100, 'default': 50, 'step': 10},
}


# Helper functions
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    conn.execute(
        "INSERT INTO chat_logs VALUES (?, ?, ?)",
        [datetime.now(), "CLEAR_CHAT", "User cleared chat history"]
    )


def extract_think_content(response):
    think_pattern = r'<think>(.*?)</think>'
    think_match = re.search(think_pattern, response, re.DOTALL)
    if think_match:
        think_content = think_match.group(1).strip()
        main_response = re.sub(think_pattern, '', response, flags=re.DOTALL).strip()
        return think_content, main_response
    return None, response


def generate_ollama_response(prompt, **params):
    # Create conversation history context
    messages = [{"role": "user", "content": prompt}]

    # Prepare the Ollama API request
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": params.get('temperature', 0.7),
            "top_p": params.get('top_p', 1.0),
            "num_predict": params.get('max_tokens', 50)
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"Error calling Ollama: {str(e)}"


# Initialize database tables
conn.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        timestamp TIMESTAMP,
        action VARCHAR,
        details VARCHAR
    )
""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        timestamp TIMESTAMP,
        role VARCHAR,
        content VARCHAR
    )
""")

# Sidebar UI
with st.sidebar:
    st.title('🐳💬 Ollama Chatbot')
    st.write('Local chatbot powered by Ollama and DuckDB')

    # Ollama configuration
    st.subheader('🦙 Ollama Settings')
    MODEL_NAME = st.selectbox(
        'Model',
        ['llama3', 'mistral', 'phi3', 'gemma', 'custom'],
        index=0
    )

    # Model parameters
    st.subheader('⚙️ Model Parameters')
    params = {
        param: st.slider(
            param.replace('_', ' ').title(),
            min_value=settings['min'],
            max_value=settings['max'],
            value=settings['default'],
            step=settings['step']
        )
        for param, settings in MODEL_PARAMS.items()
    }

    st.button('Clear Chat History', on_click=clear_chat_history)

    # Debug info
    if st.checkbox('Show debug info'):
        st.write(f"Ollama URL: {OLLAMA_URL}")
        st.write(f"Current model: {MODEL_NAME}")
        try:
            model_info = conn.execute(
                "SELECT COUNT(*) as message_count FROM chat_history"
            ).fetchdf()
            st.dataframe(model_info)
        except:
            st.warning("No chat history yet")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle user input
if prompt := st.chat_input():
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    conn.execute(
        "INSERT INTO chat_history VALUES (?, ?, ?)",
        [datetime.now(), "user", prompt]
    )

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            status_container = st.status("Thinking...", expanded=True)

            with status_container:
                response = generate_ollama_response(prompt, **params)
                think_content, main_response = extract_think_content(response)
                if think_content:
                    st.write(f"🤔 {think_content}")

            status_container.update(label="Response", state="complete", expanded=False)
            st.markdown(main_response)
            st.session_state.messages.append({"role": "assistant", "content": main_response})
            conn.execute(
                "INSERT INTO chat_history VALUES (?, ?, ?)",
                [datetime.now(), "assistant", main_response]
            )