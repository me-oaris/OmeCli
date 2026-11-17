import cv2
import numpy as np
import os
import shutil
import sys
import time

os.system("")

ASCII_CHARS = np.array(list(" .:-=+*#%@"))

def frameToAscii(frame, targetWidth=60):
    frame = cv2.flip(frame,1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    origHeight, origWidth = gray.shape
    aspectRatio = origHeight / origWidth

    targetHeight = int(targetWidth * aspectRatio * 0.5)

    resized = cv2.resize(gray, (targetWidth, targetHeight), interpolation=cv2.INTER_AREA)
    indices = (resized / 255.0 * (len(ASCII_CHARS) - 1)).astype(int)
    asciiMatrix = ASCII_CHARS[indices]

    return "\n".join("".join(row) for row in asciiMatrix)

def asciiCamera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
        return

    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cols, rows = shutil.get_terminal_size()

            width = min(70, max(20, cols -6))

            asciiArt = frameToAscii(frame, targetWidth=width)

            sys.stdout.write("\033[H" + asciiArt)
            sys.stdout.flush()

            time.sleep(1 / 20)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        sys.stdout.write("\033[?25h]")
        sys.stdout.flush()
        os.system('cls' if os.name == "nt" else "clear")
        print("Ascii Camera Intialized")

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    asciiCamera()