# state_builder.py
import cv2
import numpy as np
from collections import deque

class StateBuilder:
    """
    Keeps a stack of the last N preprocessed frames and returns
    a state tensor of shape (stack_size, H, W).
    """
    def __init__(self, stack_size=4, height=84, width=84):
        self.stack_size = stack_size
        self.height = height
        self.width = width
        self.frames = deque(maxlen=stack_size)

    def _preprocess(self, frame_bgr: np.ndarray) -> np.ndarray:
        """
        Convert BGR frame to grayscale, resize, and normalize.
        Output shape: (H, W), dtype float32 in [0,1].
        """
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (self.width, self.height), interpolation=cv2.INTER_AREA)
        normalized = resized.astype(np.float32) / 255.0
        return normalized

    def update(self, frame_bgr: np.ndarray):
        """
        Add a new frame to the stack and return the current state.
        Returns:
          - None until we have stack_size frames,
          - np.ndarray of shape (stack_size, H, W) once ready.
        """
        processed = self._preprocess(frame_bgr)
        self.frames.append(processed)

        if len(self.frames) < self.stack_size:
            return None

        state = np.stack(self.frames, axis=0)  # (stack_size, H, W)
        return state
