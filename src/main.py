from PySide6.QtWidgets import QApplication
from ui.MainWindow import MainWindow

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ✅ MainWindow 생성
    main_window = MainWindow(y=100)
    main_window.show()

    # ✅ 메인 윈도우가 숨겨져도 프로그램이 종료되지 않도록 설정
    app.exec()  # 🔥 `QApplication`을 계속 유지
