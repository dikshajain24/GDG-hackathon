import streamlit as st
import google.generativeai as genai
import requests
import re

# 🔐 Your API keys
GEMINI_API_KEY = "AIzaSyCcHC0A2GflIY2WtoaCVCYUqIWymr9He3E"  # Replace with your actual key
WEATHER_API_KEY = "869e2f8027d5a7c446a9bc1c6c1e9ee2"  # Replace with your actual key

# ✅ Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# 🌦️ Real weather fetch
def get_live_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            desc = data['weather'][0]['description'].capitalize()
            temp = round(data['main']['temp'])
            return f"{desc}, {temp}°C"
        else:
            return "Weather not found"
    except Exception as e:
        return "Error fetching weather"

# 👗 Gemini clothing suggestions
def get_clothing_suggestions(destination, month, preferences, activity, weather, category, interests):
    # Validate inputs
    if not all([destination, month, preferences, activity, weather, category, interests]):
        return "❌ Missing input fields. Please fill in all details."

    prompt = f"""
    I am planning a trip to {destination} in {month}. The weather is {weather}.
    My style preferences are {preferences}, and I’ll be doing {activity}.
    My interests include: {interests}.

    Please provide clothing recommendations suitable for this situation. Start this section with "Clothing:".

    Following that, and in a separate section starting with "Itinerary:", suggest one or two brief and specific itinerary ideas for {destination} based on my interests.
    """

    print("📝 Gemini Prompt:\n", prompt)

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Gemini API error: {str(e)}"

# 🛍️ Fake product fetch
def fetch_fake_products(keyword):
    try:
        url = "https://fakestoreapi.com/products"
        response = requests.get(url)
        if response.status_code == 200:
            products = response.json()
            return [p for p in products if keyword.lower() in p["title"].lower()]
        else:
            return []
    except Exception as e:
        return []

# 🔧 Page configuration
st.set_page_config(page_title="Gemini Travel Assistant", layout="wide")

# 💬 Gemini chatbot
st.title("💬 Gemini Chatbot - AI-Powered Assistant")
st.markdown("Ask me anything...")

prompt = st.chat_input("Talk to Gemini")
if prompt:
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    st.markdown("### 🤖 Gemini Response:")
    st.write(response.text)

# Sidebar toggle
with st.sidebar:
    st.header("✈️ Travel Assistant Menu")
    if "show_assistant" not in st.session_state:
        st.session_state.show_assistant = False

    if st.button("🧳 Open Travel Clothing Assistant"):
        st.session_state.show_assistant = True

# 🧥 Clothing Assistant UI
if st.session_state.get("show_assistant", False):
    st.title("🧳 AI-Powered Travel Clothing Assistant")

    destination = st.text_input("🌍 Destination", placeholder="e.g., Tokyo")
    month = st.selectbox("📅 Travel Month", [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ])
    preferences = st.text_input("✨ Style Preferences", placeholder="e.g., comfy, elegant, street style")
    category = st.selectbox("🧥 Clothing Type", ["Men's Clothing", "Women's Clothing"])
    activity = st.selectbox("🎯 Travel Activity", ["Sightseeing", "Beach", "Hiking", "Nightlife", "Business Trip"])
    interests = st.text_input("🎭 Interests (e.g., history, food, art)", placeholder="e.g., museums, local cuisine, architecture")

    if st.button("Get Recommendations"):
        with st.spinner("Fetching weather, outfit & itinerary ideas, and products..."):
            weather = get_live_weather(destination)
            st.success(f"📡 Current Weather in {destination}: {weather}")

            # Gemini outfit and itinerary ideas
            full_response = get_clothing_suggestions(destination, month, preferences, activity, weather, category, interests)

            st.markdown("### 🧠 Gemini Recommendations:")
            clothing_match = re.search(r"Clothing:(.*?)Itinerary:", full_response, re.DOTALL)
            itinerary_match = re.search(r"Itinerary:(.*)", full_response, re.DOTALL)

            if clothing_match:
                st.markdown("**Clothing Recommendations:**")
                st.write(clothing_match.group(1).strip())
            if itinerary_match:
                st.markdown("**Itinerary Ideas:**")
                st.write(itinerary_match.group(1).strip())
            elif not clothing_match and not itinerary_match:
                st.write(full_response) # Fallback if the expected labels aren't found

            # Fake product results
            st.markdown("### 🛍️ Matching Products from Fake Store:")
            keyword = "men" if "Men" in category else "women"
            products = fetch_fake_products(keyword)

            if products:
                for product in products[:5]:
                    st.image(product['image'], width=150)
                    st.markdown(f"**{product['title']}**")
                    st.write(product['description'])
                    st.markdown(f"[Buy Now]({product['image']})")
                    st.markdown("---")
            else:
                st.info("No matching products found.")