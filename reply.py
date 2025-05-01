import requests
import streamlit as st
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import time
import os
from dotenv import load_dotenv  # Import dotenv to load the API key

# Load environment variables from .env file
load_dotenv()

# Load the Gemini API key from the environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Debugging: Check if the API key is loaded correctly
st.write("Gemini API Key loaded:", GEMINI_API_KEY)

# Authenticate with YouTube
def youtube_authenticate():
    CLIENT_SECRET_FILE = 'C:/Users/Admin/Downloads/client_secret_562804043973-sg6ngonqh1ba5bvne7gvdhrd473dposk.apps.googleusercontent.com.json'  # Replace with your path
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_local_server()
    
    youtube = googleapiclient.discovery.build(API_NAME, API_VERSION, credentials=credentials)
    return youtube

# Function to generate personalized reply using Gemini API
def generate_personalized_reply(comment_text, api_key):
    # Correct Gemini API endpoint (replace with actual endpoint)
    gemini_endpoint = "https://api.openai.com/v1/completions"  # Replace with the correct Gemini API endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    data = {
        "model": "text-davinci-003",  # Replace with the correct model name for Gemini if different
        "prompt": f"Create a personalized response to the following comment: {comment_text}",
        "max_tokens": 100,  # Adjust token limit as needed
    }
    
    try:
        response = requests.post(gemini_endpoint, headers=headers, json=data)
        response.raise_for_status()  # Will raise an exception for 4xx or 5xx errors
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("choices", [{}])[0].get("text", "Thanks for your comment!")
        else:
            st.error(f"Error with Gemini API: {response.status_code} - {response.text}")
            return "Thanks for your comment!"
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error with Gemini API request: {str(e)}")
        return "Thanks for your comment!"

# Auto-reply to comments
def auto_reply_to_comments(youtube, video_id, api_key, reply_text="Thanks for your comment!"):
    st.write(f"📹 Fetching comments for Video ID: {video_id}")
    
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText'
    )
    
    try:
        response = request.execute()
        
        # Debugging: Log the response directly
        st.write("Raw comment response:", response)

        if 'items' in response and response['items']:
            for item in response['items']:
                comment_id = item['id']
                author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                
                # Log the comment details
                st.write(f"💬 {author} commented: {comment}")
                
                # Generate personalized reply using Gemini API
                personalized_reply = generate_personalized_reply(comment, api_key)
                st.info(f"Sending personalized auto-reply to {author}: {personalized_reply}")

                reply_request = youtube.comments().insert(
                    part='snippet',
                    body={
                        'snippet': {
                            'parentId': comment_id,
                            'textOriginal': personalized_reply
                        }
                    }
                )
                reply_response = reply_request.execute()

                # Log the reply response
                st.write(f"Reply Response: {reply_response}")
                st.success(f"✅ Replied to {author} with personalized message")

        else:
            st.write("No comments found for this video.")
            
    except googleapiclient.errors.HttpError as e:
        st.error(f"Error fetching comments or replying: {e}")

# Streamlit UI
st.title("🎥 YouTube Auto Replier with Gemini API")

# Check if Gemini API Key is loaded
if GEMINI_API_KEY:
    st.success("Gemini API Key is available.")
else:
    st.error("⚠️ Gemini API Key is not available.")

# Video ID input and reply message
video_id_input = st.text_input("Enter Video ID", "T3tBfAiwxXQ")  # Use the provided Video ID for testing
reply_text = st.text_input("Auto-reply message", value="Thanks for your comment!")

# Button to trigger the auto-reply process
if st.button("Auto Reply to Comments"):
    if video_id_input:
        st.info("🔐 Authenticating with YouTube...")
        youtube = youtube_authenticate()

        st.info("💬 Auto-replying to comments...")
        auto_reply_to_comments(youtube, video_id_input, GEMINI_API_KEY, reply_text)
    else:
        st.error("⚠️ Please enter a valid Video ID.")
