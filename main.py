import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("ui/theme.qss", "r") as f:
        app.setStyleSheet(f.read())

    win = MainWindow()
    win.show()
    sys.exit(app.exec())
