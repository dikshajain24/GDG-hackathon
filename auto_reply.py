import streamlit as st
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import time
import os

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

# Auto-reply to comments
def auto_reply_to_comments(youtube, video_id, reply_text="Thanks for your comment!"):
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
                st.info(f"Sending auto-reply to {author}")

                reply_request = youtube.comments().insert(
                    part='snippet',
                    body={
                        'snippet': {
                            'parentId': comment_id,
                            'textOriginal': reply_text
                        }
                    }
                )
                reply_response = reply_request.execute()

                # Log the reply response
                st.write(f"Reply Response: {reply_response}")
                st.success(f"✅ Replied to {author}")

        else:
            st.write("No comments found for this video.")
            
    except googleapiclient.errors.HttpError as e:
        st.error(f"Error fetching comments or replying: {e}")

# Streamlit UI
st.title("🎥 YouTube Auto Replier for Existing Video")

video_id_input = st.text_input("Enter Video ID", "T3tBfAiwxXQ")  # Use the provided Video ID for testing
reply_text = st.text_input("Auto-reply message", value="Thanks for your comment!")

if st.button("Auto Reply to Comments"):
    if video_id_input:
        st.info("🔐 Authenticating with YouTube...")
        youtube = youtube_authenticate()

        st.info("💬 Auto-replying to comments...")
        auto_reply_to_comments(youtube, video_id_input, reply_text)
    else:
        st.error("⚠️ Please enter a valid Video ID.")
