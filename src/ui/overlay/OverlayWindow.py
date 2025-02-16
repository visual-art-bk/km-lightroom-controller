from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from ui.buttons.close_btn import close_btn
from ui.utils.apply_bg_wideg_style import apply_bg_wideg_style
from ui.content_layout.TextContainerWidget import TextContainerWidget


class OverlayWindow(QWidget):
    overlay_closed = Signal()

    def __init__(self):
        super().__init__(None)  # 부모 없음 (독립 창)
        # ✅ 배경 투명 설정
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)

        self.setup_layout()

    def close_overlay(self):
        """✅ 오버레이 닫고 부모 윈도우에 신호 전달"""
        self.overlay_closed.emit()
        self.close()

    def init_position(self):
        """✅ 창을 화면 좌우 정중앙에 위치"""
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        x_pos = (screen_width - self.overlay_width) // 2
        y_pos = 18  # 고정된 Y축 위치
        self.setGeometry(x_pos, y_pos, self.overlay_width, self.overlay_height)

    def setup_layout(self):
        """전체 UI 레이아웃 설정"""
        # 오버레이 콘텐트 위젯젯
        widgetsOverlayContets = TextContainerWidget(
            file_path="오버레이메세지.txt",
            font_sizes=20,
            text_color="black",
            height=250,
        )
        width_contents = widgetsOverlayContets.width()
        height_contents = widgetsOverlayContets.height()

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(widgetsOverlayContets)

        # 메인 컨테이너
        main_container = QWidget(self)
        main_container.setObjectName("overlayMainContaier")
        styles = apply_bg_wideg_style(
            bg_color="#ffe2e0", opacity=0.9, target="#overlayMainContaier"
        )
        main_container.setStyleSheet(styles)
        main_container.setLayout(main_layout)

        # 오버레이 위치 좌우 가운데, y는 18로 설정
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        x_pos = (screen_width - width_contents) // 2
        y_pos = 18  # 고정된 Y축 위치
        self.setGeometry(x_pos, y_pos, width_contents, height_contents)

        #  absolute 포지션을 위해 나중에 추가가
        self.set_btn_close(
            main_container=main_container, width_main_contents=width_contents
        )

    def set_btn_close(self, main_container, width_main_contents):
        btn_close = close_btn()
        width_btn = btn_close.width()

        btn_close.setParent(main_container)
        btn_close.move(width_main_contents - width_btn - 10, 10)
        btn_close.clicked.connect(self.close_overlay)
