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

    def animate_text(self):
        """텍스트만 왼쪽에서 오른쪽으로 이동 후 다시 처음으로 재배치하는 애니메이션"""
        current_x = self.text.x()

        if current_x < self.width:
            self.text.move(current_x + 5, self.text.y())  # 오른쪽으로 이동
        else:
            self.text.move(-self.width // 2, self.text.y())  # 왼쪽 처음으로 되돌리기


class OverlayWindow(QWidget):
    """배경 역할을 하는 오버레이 창"""

    _instance = None  # 싱글턴 패턴 적용

    def __init__(
        self,
        width=500,
        height=250,
        bg_color="#0000FF",  # ✅ 기본값 파란색 배경
        text="Hello, Overlay!",
        text_color="yellow",  # ✅ 기본값 노란색 텍스트
        font_size=30,
        animation_speed=20,
        y_offset=100,  # ✅ Y축 위치 조정 가능
        opacity=0.5,  # ✅ 투명도 추가 (0.0 ~ 1.0)
        blur_radius=10,  # ✅ 블러 강도 추가 (0 이상)
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.y_offset = y_offset  # Y축 위치 저장
        self.bg_color = bg_color  # ✅ 배경색 저장
        self.opacity = opacity  # ✅ 투명도 저장
        self.animation_speed = animation_speed
        self.blur_radius = blur_radius  # ✅ 블러 강도 저장

        self.setWindowTitle("오버레이 창")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # ✅ 부모 `OverlayWindow`를 완전히 투명하게 설정
        self.setAttribute(Qt.WA_TranslucentBackground)

        # self.setStyleSheet(
        #     """
        #     background-color: rgba(255, 255, 255, 1);
        #     """
        # )
 

        # ✅ 배경 위젯 추가 (부모 위젯이 아니라 별도 위젯으로 투명도 적용)
        self.bg_widget = QWidget(self)

        self.bg_widget.setGeometry(0, 0, self.width, self.height)

        # ✅ 배경색과 투명도 적용
        self.apply_background_with_opacity()

        # ✅ 애니메이션 위젯 추가 (부모: self)
        self.animated_text = AnimatedTextWidget(
            text,
            text_color,
            font_size,
            self.width,
            self.height,
            animation_speed=self.animation_speed,
        )
        self.animated_text.setParent(self)  # ✅ 오버레이 창 위에 배치
        self.animated_text.setGeometry(0, 0, self.width, self.height)

        # 창 중앙 정렬
        self.center_window()

    def apply_background_with_opacity(self):
        """✅ 배경색과 투명도를 `rgba()`로 강력하게 적용"""
        r, g, b = self._hex_to_rgb(self.bg_color)

        # ✅ rgba()를 사용하여 배경색과 투명도를 동시에 적용
        self.bg_widget.setStyleSheet(
            f"background-color: rgba({r}, {g}, {b}, {self.opacity * 255});"
        )

    def _hex_to_rgb(self, hex_color):
        """HEX 색상을 RGB 값으로 변환"""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            return (
                int(hex_color[0:2], 16),
                int(hex_color[2:4], 16),
                int(hex_color[4:6], 16),
            )
        return 0, 0, 255  # 기본값 BLUE

    def center_window(self):
        """창을 화면 좌우 정가운데 위치시키고, 위아래(Y축)는 사용자 지정"""
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        x_pos = (screen_width - self.width) // 2  # 좌우 정중앙
        y_pos = min(
            max(self.y_offset, 0), screen_height - self.height
        )  # Y축 커스텀 가능

        self.setGeometry(x_pos, y_pos, self.width, self.height)

    @classmethod
    def create_overlay(cls, **kwargs):
        """싱글턴 방식으로 오버레이 창을 생성"""
        if cls._instance is None:
            cls._instance = OverlayWindow(**kwargs)
        return cls._instance

    @classmethod
    def close_overlay(cls):
        """오버레이 창을 닫는 메서드"""
        if cls._instance:
            cls._instance.close()
            cls._instance = None
