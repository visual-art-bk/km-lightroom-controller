from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from ui.overlay.TextContainerWidget import TextContainerWidget
from ui.overlay.text_contents import text_contents
from ui.utils.apply_bg_wideg_style import apply_bg_wideg_style


class OverlayWindow(QWidget):
    """배경 역할을 하는 오버레이 창"""

    _instance = None  # 싱글턴 패턴 적용

    def __init__(
        self,
        width=500,
        height=250,
        bg_color="#0000FF",  # ✅ 기본값 파란색 배경
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

        # ✅ 배경 위젯 추가 (부모 위젯이 아니라 별도 위젯으로 투명도 적용)
        self.bg_widget = QWidget(self)

        self.bg_widget.setGeometry(0, 0, self.width, self.height)
        bg_style = apply_bg_wideg_style(bg_color=self.bg_color, opacity=self.opacity)
        self.bg_widget.setStyleSheet(bg_style)

        self.text_container = TextContainerWidget(
            text_contents=text_contents,
            font_sizes=font_size,
            text_color=text_color,
            height=self.height,
        )
        self.text_container.setParent(self)
        self.text_container.setGeometry(0, 0, self.width, self.height)

        # 창 중앙 정렬
        self.center_window()

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
