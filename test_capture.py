from screen import capture_frame
import cv2

print("Capturing frame...")
frame = capture_frame()
print("Size:", frame.shape)

cv2.imshow("Game Capture Test", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
