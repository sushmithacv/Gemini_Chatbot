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
    layout="wide",  # Use a wide layout for more space
)

# Custom CSS for styling
st.markdown("""
    <style>
        .chat-message {
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
        }
        .user {
            background-color: #007bff; /* User message color */
            color: white;
            text-align: right;
        }
        .assistant {
            background-color: #f1f1f1; /* Assistant message color */
            color: black;
            text-align: left;
        }
        .streamlit-expanderHeader {
            font-size: 18px;
            font-weight: bold;
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
st.subheader("Chat with our AI Assistant")

# Display the chat history in a more organized format
for message in st.session_state.chat_session.history:
    role = translate_role_for_streamlit(message.role)
    with st.chat_message(role, key=message.id):
        st.markdown(f"<div class='chat-message {role}'>{message.parts[0].text}</div>", unsafe_allow_html=True)

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
