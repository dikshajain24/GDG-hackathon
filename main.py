import streamlit as st

# Basic example to check if Streamlit is working
st.title("Welcome to the Smart Travel Assistant")
st.write("This is a basic Streamlit app. If you see this, Streamlit is working!")

if st.button('Click Me'):
    st.write("You clicked the button!")
