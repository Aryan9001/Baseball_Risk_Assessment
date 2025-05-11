# streamlit_app.py

import streamlit as st
import os
import uuid
from main import process_video

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

st.set_page_config(page_title="Redback Baseball Risk Assessment", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: red;'>Redback Baseball Risk Assessment</h1>",
    unsafe_allow_html=True
)

st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
<b>About:</b> This tool analyzes a baseball player's movements from a video using pose estimation and joint angle analysis to assess injury risk.
Upload a video and receive a labeled output showing risk zones.
</div>
""", unsafe_allow_html=True)

uploaded_video = st.file_uploader("Upload a baseball video", type=["mp4"])

if uploaded_video is not None:
    with st.spinner("Analyzing video... hang tight!"):
        # Save input
        input_filename = f"{uuid.uuid4()}.mp4"
        input_path = os.path.join(UPLOAD_DIR, input_filename)
        with open(input_path, "wb") as f:
            f.write(uploaded_video.read())

        # Set output path
        output_filename = f"labeled_{input_filename}"
        output_path = os.path.join(PROCESSED_DIR, output_filename)

        # Process video
        process_video(input_path, output_path)

        # Display video
        st.success("✅ Analysis complete!")
        st.video(output_path)

        # Download link
        with open(output_path, "rb") as f:
            st.download_button(
                label="Download Processed Video 🎥",
                data=f,
                file_name=output_filename,
                mime="video/mp4"
            )
