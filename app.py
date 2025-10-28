import streamlit as st
from auth import auth_page
from chatbot import chatbot_ui

# Redirect to Login/Signup Page
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Welcome to LangChain Chatbot")
    st.subheader("Login or Signup")

    # Display the authentication page
    auth_page()

    st.stop()  # Prevent further execution until authenticated

# Enhanced Chatbot UI
from chatbot import chatbot_ui
chatbot_ui()