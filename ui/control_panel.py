from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QPushButton,
    QComboBox
)
from PySide6.QtCore import Signal
from ui.card import Card
from pygrabber.dshow_graph import FilterGraph


class ControlPanel(Card):

    start_clicked = Signal()
    stop_clicked = Signal()
    upload_clicked = Signal()
    camera_changed = Signal(int)
    ai_toggled = Signal(bool)

    def __init__(self):
        super().__init__()

        title = QLabel("Controls")
        title.setStyleSheet("color:white; font-weight:600;")

        # Start Button
        start_btn = QPushButton("Start")
        start_btn.setStyleSheet("background:#22c55e; color:white;")
        start_btn.clicked.connect(self.start_clicked.emit)

        # Stop Button
        stop_btn = QPushButton("Stop")
        stop_btn.setStyleSheet("background:#ef4444; color:white;")
        stop_btn.clicked.connect(self.stop_clicked.emit)

        # Upload
        upload_btn = QPushButton("Upload Video")
        upload_btn.setStyleSheet("background:#2563eb; color:white;")
        upload_btn.clicked.connect(self.upload_clicked.emit)

        # # AI Toggle
        # ai_btn = QPushButton("AI OFF")
        # ai_btn.setCheckable(True)

        # def toggle_ai():
        #     state = ai_btn.isChecked()
        #     ai_btn.setText("AI ON" if state else "AI OFF")
        #     self.ai_toggled.emit(state)

        # ai_btn.clicked.connect(toggle_ai)

        # Camera dropdown
        self.camera_select = QComboBox()
        self.camera_select.setMinimumWidth(250)
        self.camera_select.setStyleSheet("background:#2563eb; color:white;")

        self.populate_cameras()
        self.camera_select.currentIndexChanged.connect(self._emit_camera_change)

        layout = QHBoxLayout(self)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.camera_select)
        layout.addWidget(start_btn)
        layout.addWidget(stop_btn)
        layout.addWidget(upload_btn)
        # layout.addWidget(ai_btn)

    def populate_cameras(self):

        self.camera_select.clear()

        graph = FilterGraph()
        devices = graph.get_input_devices()

        if not devices:
            self.camera_select.addItem("No Camera Found", -1)
            return

        for index, name in enumerate(devices):
            self.camera_select.addItem(name, index)

        # 🔥 default select camera index 1 if exists
        if len(devices) > 1:
            self.camera_select.setCurrentIndex(1)

    def _emit_camera_change(self, index):
        device_id = self.camera_select.itemData(index)
        if device_id is not None and device_id >= 0:
            self.camera_changed.emit(device_id)
