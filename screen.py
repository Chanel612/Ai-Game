import mss
import numpy as np
import cv2

# You will resize this later to match your game window
CAPTURE_REGION = {
    "top": 200,
    "left": 300,
    "width": 800,
    "height": 600
}

sct = mss.mss()

def capture_frame():
    """Captures a screenshot of the specified region and returns a processed frame."""
    frame = np.array(sct.grab(CAPTURE_REGION))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    # optional resize to smaller image for AI
    frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
    
    return frame
