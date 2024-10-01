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
            border-radius: 10px;
            margin: 5px 0;
            max-width: 75%;
            word-wrap: break-word;
        }
        .user {
            background-color: #4caf50; /* Green for user messages */
            color: white;
            text-align: right;
            margin-left: auto; /* Align user messages to the right */
        }
        .assistant {
            background-color: #f1f1f1; /* Light gray for assistant messages */
            color: black;
            text-align: left;
            margin-right: auto; /* Align assistant messages to the left */
        }
        h1, h2 {
            color: #333; /* Darker text color for headers */
        }
        h2 {
            margin-bottom: 10px; /* Space below subheader */
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
    message_text = message.parts[0].text if message.parts else "Message not found"  # Use the correct attribute here
    with st.chat_message(role):
        st.markdown(f"<div class='chat-message {role}'>{message_text}</div>", unsafe_allow_html=True)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(f"<div class='chat-message user'>{user_prompt}</div>", unsafe_allow_html=True)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(f"<div class='chat-message assistant'>{gemini_response.parts[0].text}</div>", unsafe_allow_html=True)
