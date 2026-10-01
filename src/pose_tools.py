"""OpenCV motion analysis with an animated GIF preview for browser compatibility.

This is motion analysis, not landmark-based pose estimation.
"""
import cv2
import numpy as np
from PIL import Image

def analyze_pose_video(input_path, output_path, exercise="Squat", side="Auto", max_width=720):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError("Video file could not be opened.")
    fps = cap.get(cv2.CAP_PROP_FPS)
    fps = fps if fps and fps > 1 else 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        cap.release()
        raise ValueError("Video has invalid dimensions.")
    scale = min(1.0, max_width / width)
    out_w = max(2, int(width * scale))
    out_h = max(2, int(height * scale))
    prev = None
    reps = 0
    phase = "idle"
    frames = 0
    motion_frames = 0
    gif_frames = []
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frames += 1
            frame = cv2.resize(frame, (out_w, out_h))
            gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (7, 7), 0)
            score = 0.0
            mask = np.zeros_like(gray)
            if prev is not None:
                diff = cv2.absdiff(prev, gray)
                _, mask = cv2.threshold(diff, 22, 255, cv2.THRESH_BINARY)
                mask = cv2.dilate(mask, None, iterations=2)
                score = float(np.mean(mask > 0) * 100.0)
                if score > 0.8:
                    motion_frames += 1
                if score > 2.0:
                    phase = "moving"
                elif phase == "moving" and score < 0.6:
                    reps += 1
                    phase = "idle"
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for c in contours:
                    if cv2.contourArea(c) > 250:
                        x, y, w, h = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (40, 220, 80), 2)
            prev = gray
            label = f"Motion: {score:.1f}% | Estimated cycles: {reps}"
            cv2.rectangle(frame, (8, 8), (min(out_w-8, 560), 58), (20,20,20), -1)
            cv2.putText(frame, label, (18, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (40,220,80), 2, cv2.LINE_AA)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gif_frames.append(Image.fromarray(rgb).convert("P", palette=Image.Palette.ADAPTIVE))
    finally:
        cap.release()
    if not gif_frames:
        raise ValueError("No frames could be read from the video.")
    duration_ms = max(40, int(1000 / min(fps, 20)))
    gif_frames[0].save(output_path, save_all=True, append_images=gif_frames[1:],
                       duration=duration_ms, loop=0, optimize=False)
    return {"reps": reps, "frames": frames, "pose_frames": motion_frames, "average_angle": None,
            "note": "This analyzer uses frame-difference motion analysis, not body-joint pose estimation. The cycle count is a rough activity estimate and can be inaccurate; it is not a validated repetition counter or coaching assessment."}
