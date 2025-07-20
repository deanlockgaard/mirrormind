# ==============================================================================
# File: app.py
# Description: The main Streamlit web application interface for AI companion app.
# ==============================================================================
import streamlit as st
from engine import get_response

# --- Page Configuration ---
st.set_page_config(page_title="AI Companion", layout="wide")
st.title("🧠 AI Companion")
st.markdown("A thought partner for reflection and clarity.")

# --- Session State Initialization ---
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input ---
if prompt := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                full_response = get_response(prompt)
                message_placeholder.markdown(full_response)
            except Exception as e:
                error_message = f"An error occurred: {e}"
                message_placeholder.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

    st.session_state.messages.append({"role": "assistant", "content": full_response})