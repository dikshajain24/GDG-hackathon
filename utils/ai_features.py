import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def setup_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

def chat_with_gemini(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text
