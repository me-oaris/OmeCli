import cv2
import numpy as np

ASCII_CHARS = np.asarray(list(" .:-=+*#%@"))

class VideoEngine:
    def __init__(self, cameraIndex=0):
        self.cameraIndex = cameraIndex
        self.cap = None

    def start(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(self.cameraIndex)

    def stop(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None

    def get_ascii_frame(self, targetWidth=50):
        if self.cap is None or not self.cap.isOpened():
            self.start()

        ret, frame = self.cap.read()
        if not ret or frame is None:
            return "Starting Camera"

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        origHeight, origWidth = gray.shape
        aspectRatio = origHeight / origWidth
        targetHeight = max(5, int(targetWidth * aspectRatio * 0.5))

        resized = cv2.resize(gray, (targetWidth, targetHeight), interpolation=cv2.INTER_AREA)
        indices = (resized / 255.0 * (len(ASCII_CHARS) - 1)).astype(int)
        asciiMatrix = ASCII_CHARS[indices]

        return '\n'.join("".join(row) for row in asciiMatrix)