import streamlit as st
import requests
import uuid
import json
import time

# Configuration
WEBHOOK_URL = "https://logiqfish.app.n8n.cloud/webhook/dbchat"
BEARER_TOKEN = "FISH3055551212"  # Replace with your actual token

# App title
st.title("Chat with AI")

# Initialize session state for chat history and session ID
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    # Generate a random session ID when the app is first loaded
    st.session_state.session_id = str(uuid.uuid4())

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to call the webhook
def call_llm_webhook(user_input):
    headers = {
        #"Authorization": f"Bearer {BEARER_TOKEN}",
        "Authorization": "{BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "sessionId": st.session_state.session_id,
        "chatInput": user_input
    }
    
    try:
        response = requests.post(WEBHOOK_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response JSON
        response_data = response.json()
        
        # Extract the output from the response
        return response_data.get("output", "Sorry, I couldn't process your request.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the API: {str(e)}")
        return "Sorry, there was an error processing your request."
    
    except json.JSONDecodeError:
        st.error("Error parsing the response from the API.")
        return "Sorry, I received an invalid response format."

# Chat input and processing
if prompt := st.chat_input("What would you like to talk about?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Display assistant response with a spinner while loading
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_llm_webhook(prompt)
            st.write(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add session info in the sidebar
with st.sidebar:
    st.subheader("Session Information")
    st.write(f"Session ID: {st.session_state.session_id}")
    
    # Option to clear chat history
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
