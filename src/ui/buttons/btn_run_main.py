from constants import BTN_RUN_MAIN_BG_COLOR, BTN_RUN_MAIN_HOVER_COLOR
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


def btn_run_main():
    styles = f"""
        QPushButton {{
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 14px;
            background-color: {BTN_RUN_MAIN_BG_COLOR}; /* 버튼 배경 */
            border: 1px solid gray; /* 경계선 */
        }}
        QPushButton:hover {{
            background-color: {BTN_RUN_MAIN_HOVER_COLOR}; /* 호버 효과 */
        }}
    """
    run_button = QPushButton()
    run_button.setStyleSheet(styles)

    # ✅ 버튼에 그림자 효과 추가
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)  # ✅ 그림자 흐림 정도
    shadow.setXOffset(3)  # ✅ X축 그림자 위치
    shadow.setYOffset(3)  # ✅ Y축 그림자 위치
    shadow.setColor(QColor(0, 0, 0, 80))  # ✅ 그림자 색상 (반투명 검은색)

    run_button.setGraphicsEffect(shadow)

    button_label = QLabel(
        '<span style="color: red; font-weight: bold; font-size: 16px;">촬영</span> 시작'
    )
    button_label.setStyleSheet("color: black; font-size: 16px;")  # "시작"은 일반 크기
    button_label.setAlignment(Qt.AlignCenter)

    # QPushButton 내부에 QLabel을 배치하여 정렬
    button_layout = QHBoxLayout(run_button)
    button_layout.addWidget(button_label)
    button_layout.setAlignment(Qt.AlignCenter)  # ✅ 레이아웃 자체도 가운데 정렬
    button_layout.setContentsMargins(10, 5, 10, 5)  # ✅ 적절한 여백 설정

    return run_button
