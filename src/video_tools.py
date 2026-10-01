import cv2
import numpy as np
def analyze_video(path,max_samples=180):
    cap=cv2.VideoCapture(path)
    if not cap.isOpened(): raise ValueError("Video file could not be opened.")
    prev=None; motions=[]; events=0; preview=None; count=0
    stride=max(1,int(cap.get(cv2.CAP_PROP_FRAME_COUNT)//max_samples))
    try:
        while count<max_samples:
            ok,frame=cap.read()
            if not ok: break
            count+=1
            if count%stride: continue
            frame=cv2.resize(frame,(640,int(frame.shape[0]*640/frame.shape[1])))
            gray=cv2.GaussianBlur(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),(5,5),0)
            if prev is not None:
                diff=cv2.absdiff(prev,gray); _,mask=cv2.threshold(diff,25,255,cv2.THRESH_BINARY); mask=cv2.dilate(mask,None,iterations=2)
                contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); valid=[c for c in contours if cv2.contourArea(c)>500]
                motions.append(float(np.mean(mask>0)*100))
                if valid:
                    events+=1
                    for c in valid:
                        x, y, w, h = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            prev=gray; preview=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    finally: cap.release()
    return {"frames":len(motions),"motion_events":events,"mean_motion":float(np.mean(motions)) if motions else 0.0},preview
