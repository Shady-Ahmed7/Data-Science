import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

# Hugging Face model URL
MODEL_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

# Initialize Streamlit app
st.title("🤖 LLM-Based Chatbot")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message...")
if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare payload for Hugging Face API
    payload = {
        "inputs": user_input,
        "parameters": {
            "max_length": 200,
            "temperature": 0.7,
            "top_p": 0.9,
            "repetition_penalty": 1.2
        }
    }
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    # Call Hugging Face API
    response = requests.post(MODEL_URL, headers=headers, json=payload)

    # Process API response
    if response.status_code == 200:
        try:
            response_json = response.json()
            bot_response = response_json[0].get("generated_text", "No response received.")
        except Exception:
            bot_response = "Failed to parse response."
    else:
        bot_response = f"Error {response.status_code}: {response.text}"

    # Add bot response to session state
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(bot_response)

