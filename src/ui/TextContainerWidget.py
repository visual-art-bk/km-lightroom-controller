from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt


class TextContainerWidget(QWidget):
    """✅ QLabel을 CSS의 flexbox처럼 가운데 정렬하고, 가장 긴 텍스트에 맞게 너비 조정"""

    def __init__(self, text_contents, text_color, font_sizes, height):
        super().__init__()

        self.setFixedHeight(height)  # ✅ 높이는 고정 (가장 긴 라벨 기준이 아님)

        # ✅ font_sizes가 정수형이면 리스트로 변환
        if isinstance(font_sizes, int):
            font_sizes = [font_sizes] * len(text_contents)  # 모든 줄에 동일한 크기 적용

        # ✅ font_sizes 길이가 text_contents보다 작으면, 마지막 값으로 채움
        if len(font_sizes) < len(text_contents):
            font_sizes += [font_sizes[-1]] * (len(text_contents) - len(font_sizes))

        # ✅ 수직 레이아웃 설정 (Flexbox처럼 가운데 정렬)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)  # 줄 간격 설정
        self.layout.setContentsMargins(10, 10, 10, 10)  # 마진 추가
        self.layout.setAlignment(Qt.AlignCenter)  # ✅ 전체 레이아웃을 중앙 정렬
      

        self.labels = []  # ✅ 모든 QLabel을 저장할 리스트

        # ✅ 각 텍스트에 대해 개별 스타일 적용
        for i, text in enumerate(text_contents):
            label = QLabel(text, self)
            label.setStyleSheet(
                f"color: {text_color}; font-size: {font_sizes[i]}px; font-weight: bold; background-color: transparent;"
            )
            label.setAlignment(Qt.AlignCenter)  # ✅ 텍스트 중앙 정렬
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # ✅ 고정 크기 설정

            self.labels.append(label)  # ✅ QLabel 리스트에 저장
            self.layout.addWidget(label)  # ✅ 레이아웃에 추가

        # ✅ 가장 긴 QLabel의 너비를 가져와 `TextContainerWidget` 너비 설정
        self.adjust_to_largest_label()

    def adjust_to_largest_label(self):
        """✅ 가장 긴 QLabel의 너비에 맞춰 `TextContainerWidget` 크기 조정"""
        max_label_width = max(label.sizeHint().width() for label in self.labels)
        self.setFixedWidth(max_label_width + 20)  # ✅ 여유 공간 추가
