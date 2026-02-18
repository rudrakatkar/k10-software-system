import cv2

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # use your camera index

ret, frame = cap.read()

if ret:
    print("Resolution:", frame.shape)
    print("FPS:", cap.get(cv2.CAP_PROP_FPS))
    print("Format:", frame.dtype)
else:
    print("Failed to grab frame")

cap.release()
