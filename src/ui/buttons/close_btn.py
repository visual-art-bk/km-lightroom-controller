from PySide6.QtWidgets import QPushButton


def close_btn():
    """닫기 버튼 생성 및 스타일 적용"""
    button = QPushButton("✖")
    button.setFixedSize(30, 30)
    button.setStyleSheet(
        """
            QPushButton {
                background-color: transparent;
                font-size: 16px;
                color: black;
            }
            QPushButton:hover {
                color: red;
                font-weight: bold;
            }
        """
    )
    return button
