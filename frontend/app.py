import streamlit as st
import requests

st.title("🎬 AI Video Processing with CLIP & CUDA")

uploaded_file = st.file_uploader("Upload a video", type=["mp4"])

if uploaded_file:
    st.video(uploaded_file)
    if st.button("Process Video"):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://localhost:8000/process_video/", files=files)

        if response.status_code == 200:
            result = response.json()
            st.write("🎯 Key Moments:", result["key_moments"])
            st.write("📝 Transcript:", result["transcript"])
            st.image(result["thumbnail_path"], caption="Best Thumbnail")
