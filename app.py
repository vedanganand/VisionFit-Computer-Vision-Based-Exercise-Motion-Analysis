import os
import tempfile
from pathlib import Path

import cv2
import numpy as np
import streamlit as st

from src.image_tools import analyze_image
from src.pose_tools import analyze_pose_video
from src.video_tools import analyze_video

st.set_page_config(page_title="VisionFit", page_icon="🏃", layout="wide")
st.title("VisionFit: Fitness Movement Analyzer")
st.caption("Computer-vision exercise-video motion analysis and approximate movement-cycle counting.")
mode = st.sidebar.radio("Choose analysis", ["Fitness movement analysis", "Basic video motion", "Image processing"])
st.sidebar.info("Use a short, well-lit video with the full body visible. Results are estimates for learning and visualization, not medical advice.")

def save_upload(upload):
    suffix = Path(upload.name).suffix or ".mp4"
    f = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    f.write(upload.getbuffer()); f.close()
    return f.name

if mode == "Fitness movement analysis":
    st.subheader("Exercise-video motion analysis")
    exercise = st.selectbox("Exercise", ["Squat", "Biceps curl", "Crunch / sit-up"])
    side = st.radio("Body side to measure", ["Auto", "Left", "Right"], horizontal=True)
    up = st.file_uploader("Upload an exercise video", type=["mp4", "mov", "avi", "m4v"])
    if up and st.button("Analyze exercise", type="primary"):
        path = save_upload(up)
        out = tempfile.NamedTemporaryFile(delete=False, suffix=".gif"); out.close()
        try:
            with st.spinner("Analyzing frame-to-frame movement. Longer videos take more time..."):
                result = analyze_pose_video(path, out.name, exercise, side)
            a,b,c = st.columns(3)
            a.metric("Estimated repetitions", result["reps"])
            b.metric("Frames with movement", f'{result["pose_frames"]}/{result["frames"]}')
            c.metric("Average joint angle", f'{result["average_angle"]:.1f}°' if result["average_angle"] is not None else "—")
            with open(out.name, "rb") as preview_file:
                preview_bytes = preview_file.read()
            st.image(preview_bytes, caption="Annotated motion-analysis preview (animated GIF)", use_container_width=True)
            st.download_button("Download annotated preview", data=preview_bytes,
                               file_name="visionfit_motion_preview.gif", mime="image/gif")
            st.caption(result["note"])
            if result["pose_frames"] == 0: st.warning("Little movement was detected. Try a video with clear movement and a steady camera.")
        except Exception as e:
            st.error(f"Analysis failed: {e}")
        finally:
            for p in (path, out.name):
                try: os.unlink(p)
                except OSError: pass
elif mode == "Basic video motion":
    st.subheader("Frame-difference motion visualization")
    up = st.file_uploader("Upload a short video", type=["mp4", "mov", "avi", "m4v"])
    if up and st.button("Analyze motion"):
        path = save_upload(up)
        try:
            with st.spinner("Processing video..."):
                summary, preview = analyze_video(path)
            a,b,c=st.columns(3); a.metric("Frames sampled",summary["frames"]); b.metric("Motion frames",summary["motion_events"]); c.metric("Mean changed pixels",f'{summary["mean_motion"]:.2f}%')
            if preview is not None: st.image(preview, caption="Last sampled frame", use_container_width=True)
            st.caption("Motion frames are frame-to-frame changes, not verified exercise repetitions.")
        except Exception as e: st.error(str(e))
        finally:
            try: os.unlink(path)
            except OSError: pass
else:
    st.subheader("Image processing tools")
    up=st.file_uploader("Upload an image",type=["jpg","jpeg","png"])
    method=st.selectbox("Processing method",["Grayscale","Canny edges","Histogram equalization","Gaussian blur"])
    if up:
        data=np.frombuffer(up.read(),np.uint8); img=cv2.imdecode(data,cv2.IMREAD_COLOR)
        if img is None: st.error("Could not read image.")
        else:
            result,caption=analyze_image(img,method)
            a,b=st.columns(2); a.image(cv2.cvtColor(img,cv2.COLOR_BGR2RGB),caption="Original",use_container_width=True); b.image(result,caption=method,use_container_width=True)
            st.success(caption)
st.divider()
st.caption("This Python 3.13-compatible build uses OpenCV motion analysis. It does not estimate body joints or validate exercise form.")
