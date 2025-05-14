import streamlit as st
from huggingface_hub import InferenceClient

# Set up Hugging Face Inference Client
client = InferenceClient(
    provider="fireworks-ai",
    api_key="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",  # Replace with your actual API key
)

def ask_question(question):
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3-0324",
        messages=[{"role": "user", "content": question}],
        max_tokens=500,
    )
    return completion.choices[0].message.content

# Streamlit UI
st.title("AI Chatbot 🤖")
st.write("Ask me anything!")

# Session state for input and output
if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""

# Input box
st.session_state.question = st.text_input("Your question:", value=st.session_state.question, key="input_question")

# Button actions
col1, col2 = st.columns(2)

with col1:
    if st.button("Get Answer"):
        if st.session_state.question:
            st.session_state.answer = ask_question(st.session_state.question)
        else:
            st.warning("Please enter a question before submitting.")

with col2:
    if st.button("Clear Input & Output"):
        st.session_state.question = ""
        st.session_state.answer = ""
        st.rerun()

# Display answer
if st.session_state.answer:
    st.write("**Answer:**", st.session_state.answer)
