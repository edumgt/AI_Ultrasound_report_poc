import os
import sys
import multiprocessing as mp
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = str(BASE_DIR / "assets")
SESSIONS_DIR = str(BASE_DIR / "data" / "sessions")

def main():
    # IMPORTANT for Windows multiprocessing (spawn)
    mp.freeze_support()

    print("[app] starting...", flush=True)

    # Delay Qt/UI imports so the spawned subprocess does NOT import PySide6.
    from PySide6.QtWidgets import QApplication
    print("[app] Qt imported", flush=True)

    from ui.main_window import MainWindow
    print("[app] MainWindow imported", flush=True)

    os.makedirs(SESSIONS_DIR, exist_ok=True)

    app = QApplication(sys.argv)
    print("[app] QApplication created", flush=True)

    win = MainWindow(assets_dir=ASSETS_DIR, sessions_dir=SESSIONS_DIR)
    print("[app] MainWindow created", flush=True)
    win.resize(1000, 700)
    win.show()
    print("[app] window shown; entering event loop", flush=True)

    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("FATAL: app crashed during startup", flush=True)
        raise
