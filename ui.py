import streamlit as st

# Page setup - MUST BE THE ABSOLUTE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="DreamWeaver Assistant", layout="centered")

# --- Comprehensive Custom CSS for Dark Theme and Button Styling ---
st.markdown(
    """
    <style>
        body {
            color: #f0f2f6 !important;
            background-color: #14171a !important;
            font-family: sans-serif;
        }
        .stApp {
            background-color: #14171a !important;
        }
        .st-emotion-cache-r421ms {
            background-color: #1e2125 !important;
            color: #f0f2f6 !important;
            border-color: #80cbc4 !important;
        }
        .st-emotion-cache-r421ms input {
            color: #f0f2f6 !important;
        }
        .st-emotion-cache-1cpxqw2 {
            color: #f0f2f6 !important;
        }
        .st-emotion-cache-16txtl3 {
            background-color: #1e2125 !important;
            color: #f0f2f6 !important;
            border-right: 1px solid #1e2125 !important;
        }
        .st-emotion-cache-6qob1r a {
            color: #80cbc4 !important;
        }
        .st-emotion-cache-6qob1r a:hover {
            color: #a7ffeb !important;
        }
        .st-emotion-cache-10pw56v {
            color: #80cbc4 !important;
        }
        .st-emotion-cache-10pw56v:hover {
            color: #a7ffeb !important;
        }
        .st-emotion-cache-r421ms button {
            background-color: #26292e !important;
            color: #f0f2f6 !important;
            border-color: #80cbc4 !important;
        }
        .st-emotion-cache-r421ms button:hover {
            background-color: #303338 !important;
            color: #a7ffeb !important;
        }
        .st-emotion-cache-5rimss {
            color: #f0f2f6 !important;
        }
        .st-emotion-cache-1vbgl8p {
            background-color: #26292e !important;
            color: #80cbc4 !important;
            padding: 0.5em !important;
            border-radius: 0.3em !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #80cbc4 !important;
        }
        hr {
            background-color: #80cbc4 !important;
            height: 1px !important;
        }
        .st-emotion-cache-1y4p8pa {
            background-color: #1e2125 !important;
        }
        .st-emotion-cache-10749qb {
            color: #a7ffeb !important;
            border-bottom-color: #a7ffeb !important;
        }
        .st-emotion-cache-10749qb:hover {
            color: #a7ffeb !important;
        }
        .st-emotion-cache-504jyd {
            color: #80cbc4 !important;
        }
        .st-emotion-cache-504jyd:hover {
            color: #a7ffeb !important;
        }
        div[data-testid="stExpander"] header {
            color: #80cbc4 !important;
        }
        div[data-testid="stFileUploader"] div[data-testid="stFileUploadDropzone"] {
            background-color: #1e2125 !important;
            border-color: #80cbc4 !important;
            color: #f0f2f6 !important;
        }
        div[data-testid="stFileUploader"] div[data-testid="stFileUploadDropzone"] label {
            color: #f0f2f6 !important;
        }
        div[data-testid="stFileUploader"] div[data-testid="stFileUploadDropzone"] svg {
            fill: #80cbc4 !important;
        }
        div[data-testid="stSuccess"] {
            background-color: #2e7d32 !important;
            color: #f0f2f6 !important;
        }
        div[data-testid="stInfo"] {
            background-color: #1e88e5 !important;
            color: #f0f2f6 !important;
        }

        /* Custom Styles for Add Media Button */
        .add-media-button {
            background-color: #ffffff !important;
            color: #14171a !important;
            font-size: 18px !important;
            padding: 12px 12px !important;  /* Adjusted padding for the pin size */
            border-radius: 5px !important;
            border: 1px solid #80cbc4 !important;
            cursor: pointer;
            transition: background-color 0.3s ease, color 0.3s ease;
            width: auto !important; /* Make width flexible */
            min-width: 40px; /* Set minimum width for icon size */
            text-align: center; /* Center the text inside the button */
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .add-media-button:hover {
            background-color: #80cbc4 !important;
            color: #14171a !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ["Bot: Hello! I'm here to help you with your dreams."]
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False
if "show_plus_options" not in st.session_state:
    st.session_state.show_plus_options = False

# --- Title ---
st.title("💬 DreamWeaver Assistant")

# --- Top Section (Tabs) ---
top_tabs = st.tabs(["CREATE", "MANAGE", "ANALYZE", "MARKET"])
with top_tabs[0]:
    st.write("CREATE tab content goes here.")
with top_tabs[1]:
    st.write("MANAGE tab content goes here.")
with top_tabs[2]:
    st.write("ANALYZE tab content goes here.")
with top_tabs[3]:
    st.write("MARKET tab content goes here.")

# --- Add big vertical spacing below tabs ---
st.markdown("<div style='margin-top: 300px;'></div>", unsafe_allow_html=True)

# --- Chat Display --- 
for msg in st.session_state.chat_history:
    st.markdown(f"<div style='background-color:#26292e; color:#80cbc4; padding: 0.5em; border-radius: 0.3em;'>{msg}</div>", unsafe_allow_html=True)

# --- Chat Input Area (Modified for Gemini-like buttons) ---
input_cols = st.columns([0.85, 0.05, 0.1])
with input_cols[0]:
    user_input = st.text_input("Type your message here...", key="user_input", label_visibility="collapsed")
with input_cols[1]:
    if st.button("⋮", key="options_button"):
        st.session_state.show_sidebar = not st.session_state.show_sidebar
        st.session_state.show_plus_options = False
with input_cols[2]:
    # Only the Add Media pin button with no text
    if st.button("📎", key="add_media_button", help="Click to add media"):
        st.session_state.show_plus_options = not st.session_state.show_plus_options
        st.session_state.show_sidebar = False

# --- Handle User Message ---
if user_input:
    st.session_state.chat_history.append(f"You: {user_input}")
    st.session_state.chat_history.append("Bot: (Response coming soon...)")
    st.session_state.user_input = ""

# --- Sidebar Tools (⋮) ---
if st.session_state.show_sidebar:
    with st.expander("🎛️ Editing Tools", expanded=True):
        st.button("Crop", help="Crop coming soon.")
        st.button("Trim", help="Trim coming soon.")
        st.button("Filters", help="Filters coming soon.")

# --- Plus Tools (+) ---
elif st.session_state.show_plus_options:
    with st.expander("➕ Add to Chat", expanded=True):
        st.markdown("**Add Media**")
        
        uploaded_video = st.file_uploader("📎 Add Media", type=["mp4", "mov", "avi"], label_visibility="collapsed")
        if uploaded_video:
            st.success(f"Uploaded: {uploaded_video.name}")

        st.markdown("---")
        url_input = st.text_input("🔗 Paste a URL to analyze")
        if url_input:
            st.info(f"Analyzing: {url_input} (feature coming soon)")
