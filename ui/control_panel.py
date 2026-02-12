from PySide6.QtWidgets import QLabel, QHBoxLayout, QPushButton, QCheckBox
from ui.card import Card
from PySide6.QtCore import Signal

class ControlPanel(Card):
    ai_toggled = Signal(bool)
    upload_clicked = Signal()

    def __init__(self):
        super().__init__()

        title = QLabel("Controls")
        title.setStyleSheet("font-weight:600; font-size:14px;")

        upload_btn = QPushButton("Upload Video")
        upload_btn.setStyleSheet("""
            QPushButton {
                padding: 6px 12px;
                border-radius: 6px;
                background: #2563eb;
                color: white;
            }
        """)
        upload_btn.clicked.connect(self.upload_clicked.emit)

        ai_toggle = QCheckBox("AI Mode")
        ai_toggle.stateChanged.connect(
            lambda s: self.ai_toggled.emit(s > 0)
        )

        layout = QHBoxLayout(self)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(upload_btn)
        layout.addWidget(ai_toggle)
