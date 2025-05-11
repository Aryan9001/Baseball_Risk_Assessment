import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import os
from main import process_video
from datetime import datetime

# Set up folders
UPLOAD_DIR = "media/input_videos"
OUTPUT_DIR = "media/output_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.set_page_config(page_title="Redback Baseball Risk Assessment", layout="centered")

# Title and description
st.markdown("<h1 style='text-align: center; color: red;'>Redback Baseball Risk Assessment</h1>", unsafe_allow_html=True)
st.write("""
Upload a baseball video and we'll analyze it to detect possible injury risks using pose estimation and joint angle analysis.
This model helps assess stress on shoulders, elbows, and knees during player movements.
""")

# Upload video
uploaded_video = st.file_uploader("📤 Upload your baseball video", type=["mp4"])

if uploaded_video is not None:
    filename = uploaded_video.name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    input_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{filename}")
    output_filename = f"labeled_{timestamp}_{filename}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(input_path, "wb") as f:
        f.write(uploaded_video.read())

    with st.spinner("Analyzing video... this may take a moment ⏳"):
        process_video(input_path, output_path)

    st.success("✅ Analysis complete!")
    with open(output_path, "rb") as f:
        st.download_button("⬇️ Download analyzed video", f, file_name=output_filename, mime="video/mp4")
