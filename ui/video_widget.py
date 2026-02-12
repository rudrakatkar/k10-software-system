from PySide6.QtWidgets import QLabel, QVBoxLayout
from ui.card import Card
from PySide6.QtGui import QImage, QPixmap
import cv2

class VideoWidget(Card):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.label.setStyleSheet("background:black; border-radius:10px;")
        self.label.setScaledContents(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.addWidget(self.label)

    def update_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(img))
