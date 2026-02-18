import cv2

img = cv2.imread(r"C:\Users\Admin\Desktop\new_video.png")

cropped = img[2:25, 39+80 : 168+80]

cv2.imwrite("cropped_output.png", cropped)

print("Saved cropped_output.png")
