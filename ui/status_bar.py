from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame

class StatusBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Card")

        self.time = QLabel("04:00 PM")
        self.battery = QLabel("89%")
        self.signal = QLabel("72% Signal")
        self.sats = QLabel("Sats: 14 | HDOP: 0.8")

        layout = QHBoxLayout()
        layout.addWidget(self.time)
        layout.addStretch()
        layout.addWidget(self.signal)
        layout.addWidget(self.sats)
        layout.addWidget(self.battery)

        self.setLayout(layout)
