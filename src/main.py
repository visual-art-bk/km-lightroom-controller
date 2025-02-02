from PySide6.QtWidgets import QApplication
from ui.MainWindow import MainWindow

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ✅ Lightroom 실행기 GUI 띄우기
    main_window = MainWindow(y=50)
    main_window.show()

    sys.exit(app.exec())
