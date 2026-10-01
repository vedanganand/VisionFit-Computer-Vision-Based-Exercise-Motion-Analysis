import cv2
def analyze_image(img,method):
    if method=="Grayscale": return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),"Converted image to grayscale."
    if method=="Canny edges":
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); return cv2.Canny(gray,80,160),"Detected image edges using Canny."
    if method=="Histogram equalization":
        ycrcb=cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb); ycrcb[:,:,0]=cv2.equalizeHist(ycrcb[:,:,0]); return cv2.cvtColor(ycrcb,cv2.COLOR_YCrCb2RGB),"Enhanced luminance contrast using histogram equalization."
    return cv2.cvtColor(cv2.GaussianBlur(img,(7,7),0),cv2.COLOR_BGR2RGB),"Applied Gaussian smoothing."
