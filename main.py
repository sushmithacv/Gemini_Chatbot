import os
import streamlit as st
from googletrans import Translator
import googlemaps
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import speech_recognition as sr
from gtts import gTTS
import requests
import dialogflow_v2 as dialogflow
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Initialize external services
translator = Translator()
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

# Streamlit page settings
st.set_page_config(
    page_title="Enhanced ChatBot",
    page_icon=":robot:",
    layout="centered",
)

st.title("🤖 Enhanced ChatBot with Voice, Translation, APIs")

# Speech-to-text function
def listen_to_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        st.write(f"**You said**: {user_input}")
        return user_input
    except sr.UnknownValueError:
        st.error("Sorry, I did not understand.")
    except sr.RequestError:
        st.error("Could not request results from the Speech Recognition service.")
    return ""

# Text-to-speech function
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name + ".mp3")
        st.audio(fp.name + ".mp3")

# Translate text function
def translate_text(text, dest_language='es'):
    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

# Dialogflow response
def get_dialogflow_response(text, session_id="current_user", language_code='en'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text

# Spotify music search
def search_spotify_music(query):
    result = sp.search(q=query, type='track', limit=1)
    if result['tracks']['items']:
        track = result['tracks']['items'][0]
        return f"Listen on Spotify: {track['external_urls']['spotify']}"
    else:
        return "No tracks found."

# YouTube video search
def search_youtube(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    if results:
        video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
        return f"Watch on YouTube: {video_url}"
    else:
        return "No videos found."

# Google Maps search
def get_location_info(query):
    result = gmaps.places(query)
    if result['results']:
        return result['results'][0]['formatted_address']
    else:
        return "Location not found."

# Chatbot functionalities display
st.sidebar.subheader("Features")
voice_input = st.sidebar.checkbox("Voice Input/Output")
translation_enabled = st.sidebar.checkbox("Enable Language Translation")
multi_turn_enabled = st.sidebar.checkbox("Enable Multi-turn Conversations")
external_api_enabled = st.sidebar.checkbox("Integrate External APIs")

# Voice input handling
if voice_input:
    user_prompt = listen_to_voice()
else:
    user_prompt = st.text_input("Type your message")

if user_prompt:
    if translation_enabled:
        language = st.selectbox("Select Language for Translation", ['es', 'fr', 'de', 'it', 'zh-cn', 'hi'])
        translated_text = translate_text(user_prompt, dest_language=language)
        st.write(f"**Translated Text**: {translated_text}")
        user_prompt = translated_text

    if multi_turn_enabled:
        dialogflow_response = get_dialogflow_response(user_prompt)
        st.write(f"🤖: {dialogflow_response}")
        speak_text(dialogflow_response)
    else:
        st.write(f"🤖: {user_prompt}")

    if external_api_enabled:
        st.subheader("External API Integrations")
        
        if st.checkbox("Spotify Music Search"):
            music_query = st.text_input("Search for music:")
            if music_query:
                spotify_link = search_spotify_music(music_query)
                st.write(spotify_link)
        
        if st.checkbox("YouTube Video Search"):
            video_query = st.text_input("Search for a video:")
            if video_query:
                youtube_link = search_youtube(video_query)
                st.write(youtube_link)
        
        if st.checkbox("Google Maps Search"):
            location_query = st.text_input("Search for a place:")
            if location_query:
                location_info = get_location_info(location_query)
                st.write(location_info)
