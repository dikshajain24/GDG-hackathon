import google.generativeai as genai

# 🔐 Directly set your API key (replace with your new one)
GEMINI_API_KEY = "AIzaSyCcHC0A2GflIY2WtoaCVCYUqIWymr9He3E"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# List available models
try:
    models = genai.list_models()
    for model in models:
        print(model.name)
except Exception as e:
    print(f"Error listing models: {str(e)}")
