# test_capture.py
from screen import capture_frame
import cv2
import time

print("Starting live screen capture...")

while True:
    frame = capture_frame()
    cv2.imshow("Live Capture", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
from screen import capture_frame
import cv2

print("Capturing frame...")
frame = capture_frame()
print("Size:", frame.shape)

cv2.imshow("Game Capture Test", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
