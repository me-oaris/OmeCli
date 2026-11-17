import cv2

def camera_feed():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Webcam couldn't open")
        return
    print("Welcome Initilized! Press `q` to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Idk error --")
            break

        cv2.imshow("OmeCli Video Engine", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_feed()