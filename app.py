from __future__ import annotations
import sys, os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SESSIONS_DIR = os.path.join(BASE_DIR, "data", "sessions")

def main():
    app = QApplication(sys.argv)
    win = MainWindow(assets_dir=ASSETS_DIR, sessions_dir=SESSIONS_DIR)
    win.resize(1000, 900)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
