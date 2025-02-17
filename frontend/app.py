import streamlit as st
import requests
import json

st.title("AI-Powered Video Processing")

uploaded_file = st.file_uploader("Upload a video", type=["mp4"])

if uploaded_file is not None:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post("http://localhost:8000/process_video/", files=files)
    
    if response.status_code == 200:
        data = response.json()
        st.subheader("Key Moments")
        st.write(data["key_moments"])
        
        st.subheader("Transcript")
        st.write(data["transcript"])
        
        st.subheader("Generated Thumbnail")
        st.image(data["thumbnail"])
