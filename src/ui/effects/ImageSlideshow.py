from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QStackedWidget,
    QGraphicsOpacityEffect,
    QSizePolicy,
    QVBoxLayout,
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation
from PySide6.QtGui import QPixmap

DURATION_PLAY = 5500
DURATION_FADEIN = 1250
DURATION_FADEOUT = 500


class ImageSlideshow(QWidget):
    def __init__(
        self, width, height, aspect_ratio_mode=Qt.KeepAspectRatio, text_size=48
    ):
        """
        :param width: 슬라이드쇼 너비
        :param height: 슬라이드쇼 높이
        :param aspect_ratio_mode: 이미지 비율 조정 방식 (기본: Qt.KeepAspectRatio)
        :param text_size: 텍스트 크기 (기본값: 24px)
        """
        super().__init__()

        self.setFixedSize(width, height)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # ✅ 여러 이미지를 담는 QStackedWidget (텍스트를 이미지 위에 배치할 수 있도록 함)
        self.stack = QStackedWidget(self)
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack.setContentsMargins(0, 0, 0, 0)
        self.stack.setStyleSheet("border: none;")  # ✅ 보더 제거

        self.aspect_ratio_mode = aspect_ratio_mode  # ✅ 사용자 지정 비율 모드 저장
        self.text_size = text_size  # ✅ 텍스트 크기 저장
        self.images = [
            ("image1.jpg", "오늘은, 내일의 추억입니다"),
            ("image2.jpg", "영원한 정지 화면으로 간직합니다"),
            ("image3.jpg", "나의 사진은 나의 지금이다"),
            ("image4.jpg", "다비 스튜디오에서 특별한 기억을"),
        ]
        self.containers = []  # ✅ 이미지 + 텍스트 컨테이너 저장
        self.effects = []

        for img_path, text in self.images:
            # ✅ 컨테이너 생성 (이미지 + 텍스트를 겹칠 컨테이너)
            container = QWidget()
            container.setFixedSize(width, height)
            container.setStyleSheet(
                "background-color: transparent;"
            )  # ✅ 배경 투명 설정

            # ✅ 이미지 라벨 (백그라운드)
            img_label = QLabel(container)
            img_label.setFixedSize(width, height)
            pixmap = QPixmap(img_path)

            # ✅ 사용자 지정 비율에 따라 크기 조정
            scaled_pixmap = pixmap.scaled(
                width, height, self.aspect_ratio_mode, Qt.SmoothTransformation
            )
            img_label.setPixmap(scaled_pixmap)
            img_label.setAlignment(Qt.AlignCenter)

            # ✅ 텍스트 라벨 (이미지 위에 올리기)
            text_label = QLabel(text, container)
            text_label.setStyleSheet(
                f"""
                color: white; 
                font-size: {self.text_size}px; 
                font-weight: bold;
                background-color: transparent;
            """
            )
            text_label.setFixedSize(width, height)
            text_label.setAlignment(Qt.AlignCenter)  # ✅ 텍스트를 가로, 세로 중앙 정렬

            # ✅ 투명도 효과 추가 (애니메이션 적용 가능)
            effect = QGraphicsOpacityEffect()
            container.setGraphicsEffect(effect)
            effect.setOpacity(0.0)
            self.effects.append(effect)

            self.stack.addWidget(container)
            self.containers.append(container)

        self.effects[0].setOpacity(1.0)
        self.stack.setCurrentIndex(0)

        # ✅ 올바른 레이아웃 설정 (QVBoxLayout을 사용하여 QStackedWidget 추가)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)  # ✅ QStackedWidget을 추가
        self.setLayout(layout)  # ✅ 오류 발생하지 않도록 setLayout에 QVBoxLayout 전달

        self.fade_out = QPropertyAnimation(self.effects[0], b"opacity")
        self.fade_out.setDuration(DURATION_FADEOUT)

        self.fade_in = QPropertyAnimation(self.effects[0], b"opacity")
        self.fade_in.setDuration(DURATION_FADEIN)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_image)
        self.timer.start(DURATION_PLAY)

        self.current_index = 0

    def next_image(self):
        old_index = self.current_index
        self.current_index = (self.current_index + 1) % len(self.containers)

        self.fade_out.setTargetObject(self.effects[old_index])
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.finished.connect(lambda: self.complete_switch(old_index))
        self.fade_out.start()

    def complete_switch(self, old_index):
        """✅ 페이드아웃이 끝난 후에만 이미지 변경"""
        self.stack.setCurrentIndex(self.current_index)
        self.effects[old_index].setOpacity(1.0)

        self.fade_in.setTargetObject(self.effects[self.current_index])
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.start()
