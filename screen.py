# screen.py
import mss
import numpy as np
import cv2

sct = mss.mss()

def capture_frame():
    """Capture the entire primary screen and downscale it."""
    monitor = sct.monitors[1]   # primary display
    frame = np.array(sct.grab(monitor))       # BGRA
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
    return frame
# screen.py - macOS full screen capture with visible cursor
import Quartz
import numpy as np
import cv2
import pyautogui

def capture_frame():
    # Capture full screen screenshot (always includes cursor)
    screenshot = Quartz.CGWindowListCreateImage(
        Quartz.CGRectInfinite,
        Quartz.kCGWindowListOptionOnScreenOnly,
        Quartz.kCGNullWindowID,
        Quartz.kCGWindowImageDefault
    )

    width = Quartz.CGImageGetWidth(screenshot)
    height = Quartz.CGImageGetHeight(screenshot)

    # Extract raw buffer
    provider = Quartz.CGImageGetDataProvider(screenshot)
    data = Quartz.CGDataProviderCopyData(provider)
    img = np.frombuffer(data, dtype=np.uint8)
    img = img.reshape((height, width, 4))  # BGRA

    # Convert BGRA → BGR
    img = img[:, :, :3]

    # Resize for performance
    img = cv2.resize(img, (1280, 720))

    return img
# screen.py  (macOS guaranteed cursor overlay)
import mss
import numpy as np
import cv2
import Quartz
import pyautogui

sct = mss.mss()

def get_cursor_image():
    """Returns the actual macOS cursor image and hotspot offset."""
    cursor = Quartz.CGDisplayCopyCursorImage(Quartz.CGMainDisplayID())
    width = Quartz.CGImageGetWidth(cursor)
    height = Quartz.CGImageGetHeight(cursor)
    hotspot = Quartz.CGImageGetHotSpot(cursor)

    # Extract raw image
    provider = Quartz.CGImageGetDataProvider(cursor)
    data = Quartz.CGDataProviderCopyData(provider)
    pixels = np.frombuffer(data, dtype=np.uint8)
    pixels = pixels.reshape((height, width, 4))  # RGBA

    return pixels, hotspot

def capture_frame():
    """Capture screen and overlay real macOS cursor."""
    monitor = sct.monitors[1]
    frame = np.array(sct.grab(monitor))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # Resize for display (doesn't break cursor alignment)
    target_w, target_h = 1280, 720
    frame = cv2.resize(frame, (target_w, target_h))

    # Get the real mouse pos
    mx, my = pyautogui.position()

    # Scale cursor to match resized frame
    scale_x = target_w / monitor["width"]
    scale_y = target_h / monitor["height"]

    fx = int(mx * scale_x)
    fy = int(my * scale_y)

    # Get actual cursor image
    cursor_img, hotspot = get_cursor_image()
    cw, ch = cursor_img.shape[1], cursor_img.shape[0]

    # Compute draw region
    top = fy - hotspot.y
    left = fx - hotspot.x
    bottom = top + ch
    right = left + cw

    # Clip if cursor near edge
    if top < 0: top = 0
    if left < 0: left = 0
    if bottom > target_h: bottom = target_h
    if right > target_w: right = target_w

    # Extract region and blend cursor
    roi = frame[top:bottom, left:right]
    cursor_rgba = cursor_img[0:(bottom-top), 0:(right-left)]

    # Alpha blending
    alpha = cursor_rgba[..., 3:] / 255.0
    frame[top:bottom, left:right] = (1 - alpha) * roi + alpha * cursor_rgba[..., :3]

    return frame
# screen.py
import mss
import numpy as np
import cv2
import pyautogui

sct = mss.mss()

def get_scale_factor():
    # Grab a tiny screenshot and compare sizes
    monitor = sct.monitors[1]
    test = sct.grab(monitor)
    return test.width / monitor["width"]

def capture_frame():
    """Capture entire screen and overlay mouse cursor (Retina-compatible)."""
    monitor = sct.monitors[1]

    screen_w = monitor["width"]
    screen_h = monitor["height"]

    # Retina fix
    scale = get_scale_factor()

    # Capture raw frame
    raw = sct.grab(monitor)
    frame = np.array(raw)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # Resize for display
    target_w, target_h = 640, 360
    frame = cv2.resize(frame, (target_w, target_h))

    # Mouse position (in 1× coords)
    mx, my = pyautogui.position()

    # Convert to 2× Retina coords if necessary
    mx_scaled = mx * scale
    my_scaled = my * scale

    # Map to resized window
    fx = int(mx_scaled * (target_w / raw.width))
    fy = int(my_scaled * (target_h / raw.height))

    # Draw cursor
    cv2.circle(frame, (fx, fy), 7, (0, 255, 0), -1)

    return frame
# screen.py
import mss
import numpy as np
import cv2
import pyautogui

sct = mss.mss()

def capture_frame():
    """Capture entire screen and overlay mouse cursor."""
    monitor = sct.monitors[1]  # main display

    # Get screen size for cursor mapping
    screen_w = monitor["width"]
    screen_h = monitor["height"]

    # Capture full screen
    frame = np.array(sct.grab(monitor))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # Resize frame (optional)
    target_w, target_h = 640, 360
    frame = cv2.resize(frame, (target_w, target_h))

    # Overlay mouse cursor
    mx, my = pyautogui.position()

    # Map cursor to resized frame coordinates
    fx = int(mx * (target_w / screen_w))
    fy = int(my * (target_h / screen_h))

    # Draw the mouse cursor as a green dot
    cv2.circle(frame, (fx, fy), 7, (0, 255, 0), -1)

    return frame
# screen.py
import mss
import numpy as np
import cv2

sct = mss.mss()

def capture_frame():
    """Capture the entire primary screen."""
    monitor = sct.monitors[1]   # monitor[1] = main display
    frame = np.array(sct.grab(monitor))

    # Remove alpha channel BGRA → BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # Optional: resize to something manageable for AI
    frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)

    return frame
