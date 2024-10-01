import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #eaeaea;
        font-family: Arial, sans-serif;
    }
    .chat-message {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        max-width: 80%;
    }
    .user {
        background-color: #d1e7dd; /* Light green */
        text-align: right;
        color: #0f5132;
    }
    .assistant {
        background-color: #fff3cd; /* Light yellow */
        color: #856404;
        text-align: left;
    }
    .copy-button {
        margin-top: 5px;
        background-color: #007bff; /* Bootstrap primary blue */
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        padding: 5px 10px;
    }
    .copy-button:hover {
        background-color: #0056b3; /* Darker blue */
    }
    </style>
""", unsafe_allow_html=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("Gemini Pro - ChatBot")

# Function to copy text to clipboard
def copy_to_clipboard(text):
    st.markdown(f"<script>navigator.clipboard.writeText('{text}'); alert('Copied to clipboard!');</script>", unsafe_allow_html=True)

# Display the chat history in a more organized format
for message in st.session_state.chat_session.history:
    role = translate_role_for_streamlit(message.role)
    chat_content = message.parts[0].text if role == "assistant" else message.content

    with st.chat_message(role):
        st.markdown(f"<div class='chat-message {role}'>{chat_content}</div>", unsafe_allow_html=True)
        
        # Copy button for assistant messages
        if role == "assistant":
            st.button("Copy Response", key=f"copy_{message.id}", help="Copy this response to clipboard", 
                      on_click=copy_to_clipboard, args=(chat_content,))

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(f"<div class='chat-message user'>{user_prompt}</div>", unsafe_allow_html=True)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(f"<div class='chat-message assistant'>{gemini_response.text}</div>", unsafe_allow_html=True)
        st.button("Copy Response", key="copy_response", help="Copy this response to clipboard", 
                  on_click=copy_to_clipboard, args=(gemini_response.text,))
