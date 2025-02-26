from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
from typedefs.main_window_types import SizeDict


class TypingEffectDisplay(QWidget):
    def __init__(self, size: SizeDict, text, parent=None):
        super().__init__(parent)
        self.width = size.get("width")
        self.height = size.get("height")
        self.full_text = text
        self.current_text = ""
        self.index = 0

        # ✅ 스타일 적용
        self.setFixedSize(self.width, self.height)

        # ✅ QLabel 생성 (텍스트 출력용)
        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # ✅ 왼쪽 정렬
        self.label.setStyleSheet("font-size: 16px; color: #55624C; font-weight: 600")
        self.label.setWordWrap(True)  # ✅ 자동 줄바꿈 활성화
        self.label.setFixedWidth(
            self.width - 24
        )  # ✅ 너비를 부모 width에 맞게 제한 (padding 고려)

        # ✅ QVBoxLayout 적용 (여러 줄 표시 가능하도록 설정)
        text_layout = QVBoxLayout()
        text_layout.addWidget(self.label)
        text_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # ✅ 텍스트 왼쪽 정렬

        # ✅ QHBoxLayout 적용 (전체 배경 정렬 문제 해결)
        wrapper_layout = QHBoxLayout(self)
        wrapper_layout.addLayout(text_layout)
        wrapper_layout.setAlignment(
            Qt.AlignLeft | Qt.AlignTop
        )  # ✅ 배경도 왼쪽 정렬 유지
        wrapper_layout.setContentsMargins(4, 32, 4, 4)  # ✅ 불필요한 마진 제거
        self.setLayout(wrapper_layout)

        # ✅ QTimer로 타이핑 효과 구현
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(50)  # 50ms마다 한 글자씩 출력

    def update_text(self):
        """한 글자씩 추가하여 텍스트를 표시 (자동 줄바꿈 적용)"""
        if self.index < len(self.full_text):
            self.current_text += self.full_text[self.index]
            self.label.setText(self.current_text)
            self.index += 1
        else:
            self.timer.stop()  # 문장이 다 출력되면 타이머 정지

    def set_text(self, text):
        """디스플레이에 새로운 문장을 설정하고 타이핑 효과 시작"""
        self.full_text = text
        self.current_text = ""
        self.index = 0
        self.label.setText("")  # 기존 텍스트 초기화
        self.timer.start(50)  # 타이핑 애니메이션 재시작


def create_main_display_widget(size: SizeDict):
    """챗GPT 같은 타이핑 애니메이션이 적용된 디스플레이 위젯"""
    try:
        with open("메시지/디스플레이메시지.txt", "r", encoding="utf-8") as file:
            text = file.read().strip()
    except FileNotFoundError:
        text = "디스플레이 메시지를 불러올 수 없습니다."

    return TypingEffectDisplay(size, text)
