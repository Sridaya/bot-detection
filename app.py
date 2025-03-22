import streamlit as st
import requests

st.title("Twitter Bot Detection Tool")

username = st.text_input("Enter Twitter Username:")
if st.button("Check Bot"):
    response = requests.get(f"http://127.0.0.1:10000/check-bot/?username={username}")
    result = response.json()
    st.write("Bot Status:", "🚨 Bot" if result["is_bot"] else "✅ Human")
