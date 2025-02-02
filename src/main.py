from PySide6.QtWidgets import QApplication
from ui.MainWindow import MainWindow
from ui.overlay.OverlayWindow import OverlayWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ✅ 오버레이 창 생성 (배경색과 투명도 정상 적용됨)
    overlay = OverlayWindow.create_overlay(
        width=1200,
        height=550,
        bg_color="#FFFFFF",  # ✅ 배경색 (파란색)
        opacity=0.3,  # ✅ 투명도 50%
        text="⚠ 경고: 설정을 변경하지 마세요!",
        text_color="black",  # ✅ 텍스트 색상 설정 가능
        font_size=48,
        animation_speed=25,  # ✅ 애니메이션 속도 조정 가능
        y_offset=50,  # ✅ Y축 위치 조정 가능
        blur_radius=50,
    )
    overlay.show()

    x_position = None  # None을 사용하면 자동으로 우측 끝으로 배치
    y_position = 100  # 화면 꼭대기
    window_width = 300  # 창 너비
    window_height = 200  # 창 높이

    main_window = MainWindow(
        x=x_position, y=y_position, width=window_width, height=window_height
    )
    main_window.show()

    sys.exit(app.exec())
