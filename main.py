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
    layout="wide",  # Use a wider layout for better space utilization
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f5;  /* Light background color */
    }
    .chat-container {
        background-color: #ffffff;  /* Chat bubble background */
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        max-width: 600px;
        margin: auto;
    }
    .user-message {
        background-color: #d1e7dd;  /* Light green for user messages */
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        text-align: right;
    }
    .assistant-message {
        background-color: #f8d7da;  /* Light red for assistant messages */
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the chatbot's title and instructions on the page
st.title("🤖 Gemini Pro - ChatBot")
st.write("Ask me anything, and I'll do my best to assist you!")

# Create a container for chat messages
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display the chat history
    for message in st.session_state.chat_session.history:
        role = translate_role_for_streamlit(message.role)
        if role == "user":
            message_class = "user-message"
        else:
            message_class = "assistant-message"

        # Display each message
        with st.container(class_=message_class):
            st.markdown(message.parts[0].text)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

# Add a footer for extra information or links
st.markdown(
    """
    <footer style='text-align: center; margin-top: 20px;'>
        <p>Powered by <a href="https://generativeai.google/" target="_blank">Google Generative AI</a></p>
    </footer>
    """,
    unsafe_allow_html=True
)
