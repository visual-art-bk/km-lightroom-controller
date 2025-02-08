from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsBlurEffect
from PySide6.QtCore import Qt, QTimer


class AnimatedTextWidget(QWidget):
    """텍스트 애니메이션을 위한 개별 위젯"""

    def __init__(self, text, text_color, font_size, width, height, animation_speed=20):
        super().__init__()

        self.width = width
        self.height = height

        # ✅ 텍스트 라벨 추가 (배경 없음)
        self.text = QLabel(text, self)
        self.text.setStyleSheet(
            f"color: {text_color}; font-size: {font_size}px; font-weight: bold; background-color: transparent;"
        )
        self.text.setAlignment(Qt.AlignVCenter)  # 세로 정렬 중앙
        self.text.move(
            -self.width // 2, self.height // 2 - font_size
        )  # 시작 위치 (왼쪽 밖)

        self.animation_speed = animation_speed

        # ✅ 애니메이션 타이머 (텍스트 이동)
        self.move_animation = QTimer(self)
        self.move_animation.timeout.connect(self.animate_text)
        self.move_animation.start(self.animation_speed)  # ✅ 기본 애니메이션 속도