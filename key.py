import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the API key is loaded
if not GEMINI_API_KEY:
    print("⚠️ Gemini API Key not found. Please check your .env file.")
else:
    print("✅ Gemini API Key loaded successfully.")

# Function to test Gemini API
def test_gemini_api():
    # Sample message to test the API
    test_comment = "This is a test comment to generate a response."

    # Define the Gemini API endpoint
    gemini_api_url = "https://generativeai.googleapis.com/v1beta2/chat:sendMessage"  # Update the endpoint if needed

    # Prepare the headers with the API key
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }

    # Prepare the data payload for the request
    data = {
        "message": test_comment,
        "model": "gemini-2.0",  # Update the model as needed
    }

    # Send a POST request to Gemini API
    response = requests.post(gemini_api_url, json=data, headers=headers)

    # Check the response status and print results
    if response.status_code == 200:
        response_data = response.json()
        print("🎉 Success! Generated response:", response_data.get("text", "No response text found"))
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

# Run the test
test_gemini_api()
