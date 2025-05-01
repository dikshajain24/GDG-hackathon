# streamlit_app.py

import streamlit as st
import os
import uuid
import requests
from PIL import Image
from io import BytesIO
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import google.generativeai as genai

# Gemini API Key
GEMINI_API_KEY = "your-gemini-key-here"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def generate_script(prompt):
    response = model.generate_content(f"Write a short, catchy 15-second video ad script for: {prompt}")
    return response.text.strip()

def fetch_images(prompt):
    keywords = prompt.split()[:3]
    images = []
    for word in keywords:
        url = f"https://source.unsplash.com/800x450/?{word}"
        img_data = requests.get(url).content
        img = Image.open(BytesIO(img_data))
        images.append(img)
    return images

def create_voiceover(text):
    tts = gTTS(text)
    audio_path = f"{uuid.uuid4().hex}_voice.mp3"
    tts.save(audio_path)
    return audio_path

def make_video(images, audio_path):
    clips = []
    for img in images:
        img_path = f"{uuid.uuid4().hex}.png"
        img.save(img_path)
        clip = ImageClip(img_path).set_duration(5)
        clips.append(clip)

    video = concatenate_videoclips(clips)
    audio = AudioFileClip(audio_path)
    final = video.set_audio(audio)
    
    video_path = f"{uuid.uuid4().hex}_final_video.mp4"
    final.write_videofile(video_path, codec="libx264", audio_codec="aac")
    return video_path

# Streamlit UI
st.set_page_config(page_title="AdGenie", layout="centered")
st.title("🎥 AdGenie: AI Video Ad Generator")

user_input = st.text_input("📝 Describe your product or idea:", placeholder="e.g. A fitness app for busy moms")

if st.button("🚀 Generate Ad"):
    if not user_input:
        st.warning("Please enter a product description.")
    else:
        with st.spinner("Writing ad script..."):
            script = generate_script(user_input)
            st.success("✅ Script ready!")
            st.text_area("🗣️ Ad Script:", script)

        with st.spinner("Fetching images..."):
            imgs = fetch_images(user_input)

        with st.spinner("Creating voiceover..."):
            audio = create_voiceover(script)

        with st.spinner("Rendering video..."):
            video = make_video(imgs, audio)

        st.success("🎉 Ad ready!")
        st.video(video)
