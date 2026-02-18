import sys
import cv2
import time
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen
from PySide6.QtCore import Qt, QRect, QTimer


CAMERA_INDEX = 1   # 🔥 Your USB camera index


class ROIWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ROI Selector - SPACE = Pause/Play")

        # -----------------------------
        # Open Camera
        # -----------------------------
        self.cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            print("❌ Failed to open camera")
            return

        # OPTIONAL: Force 1080p
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_FPS, 60)

        # -----------------------------
        # Print Camera Properties
        # -----------------------------
        width  = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps    = self.cap.get(cv2.CAP_PROP_FPS)
        fourcc = int(self.cap.get(cv2.CAP_PROP_FOURCC))

        print("\n===== CAMERA INFO =====")
        print("Resolution :", width, "x", height)
        print("FPS (reported):", fps)
        print("FOURCC:", fourcc)
        print("=======================\n")

        # -----------------------------
        # Runtime Variables
        # -----------------------------
        self.current_frame = None
        self.playing = True
        self.start_point = None
        self.end_point = None

        self.prev_time = time.time()

        self.label = QLabel(self)
        self.setCentralWidget(self.label)

        # Timer (~60 FPS)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(16)

    # -----------------------------
    # Video playback
    # -----------------------------
    def update_frame(self):

        if not self.playing:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        # ---- Measure REAL FPS ----
        current_time = time.time()
        real_fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        print(f"Real FPS: {real_fps:.2f}", end="\r")

        self.current_frame = frame
        self.show_frame()

    def show_frame(self):

        if self.current_frame is None:
            return

        rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape

        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        self.label.setPixmap(pixmap)
        self.resize(w, h)

    # -----------------------------
    # Mouse handling (ROI)
    # -----------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = None

    def mouseMoveEvent(self, event):
        if self.start_point:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_point:
            self.end_point = event.pos()

            x1 = self.start_point.x()
            y1 = self.start_point.y()
            x2 = self.end_point.x()
            y2 = self.end_point.y()

            print("\n===== ROI Selected =====")
            print(f"Start: ({x1}, {y1})")
            print(f"End:   ({x2}, {y2})")
            print(
                f"Use in code: frame[{min(y1,y2)}:{max(y1,y2)}, "
                f"{min(x1,x2)}:{max(x1,x2)}]"
            )
            print("========================\n")

            self.start_point = None
            self.end_point = None
            self.update()

    # -----------------------------
    # Draw rectangle
    # -----------------------------
    def paintEvent(self, event):
        super().paintEvent(event)

        if self.start_point and self.end_point:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.green, 2))
            rect = QRect(self.start_point, self.end_point)
            painter.drawRect(rect)

    # -----------------------------
    # Keyboard controls
    # -----------------------------
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.playing = not self.playing
            print("PLAYING" if self.playing else "PAUSED")


def main():
    app = QApplication(sys.argv)
    window = ROIWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
