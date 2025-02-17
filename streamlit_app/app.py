# streamlit_app/app.py
import streamlit as st
import requests
import tempfile

st.title("AI-Powered Video Clipping & Summarization Tool")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])
if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    st.video(temp_file_path)

    if st.button("Process Video"):
        with open(temp_file_path, "rb") as f:
            files = {"file": f}
            # Adjust the URL if your FastAPI backend is hosted elsewhere
            response = requests.post("http://localhost:8000/process_video", files=files)
        if response.status_code == 200:
            result = response.json()
            st.subheader("Generated Caption")
            st.write(result.get("caption", ""))
            st.subheader("Best Scene (start, end in sec)")
            st.write(result.get("best_scene", ""))
            st.subheader("Sentiment Analysis")
            st.write(result.get("sentiments", ""))
        else:
            st.error("Error processing video.")
