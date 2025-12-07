# success_detector.py
import cv2
import numpy as np

class ActionSuccessDetector:
    """
    Game-agnostic: if the frame after a key press is significantly
    different from the frame before, we say the action 'worked'.
    """

    def __init__(self, diff_threshold=0.03):
        """
        diff_threshold: how much average pixel change is needed (0–1).
        Lower = more sensitive, higher = stricter.
        """
        self.diff_threshold = diff_threshold

    def action_succeeded(self, prev_frame_bgr: np.ndarray, next_frame_bgr: np.ndarray) -> bool:
        prev_gray = cv2.cvtColor(prev_frame_bgr, cv2.COLOR_BGR2GRAY)
        next_gray = cv2.cvtColor(next_frame_bgr, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, next_gray)
        score = diff.mean() / 255.0
        # You can print for debugging if you want:
        # print(f"[DETECTOR] diff score={score:.4f}")
        return score > self.diff_threshold
