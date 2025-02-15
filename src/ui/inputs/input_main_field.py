from constants import MAIN_WINDOW_BG_COLOR
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QVBoxLayout,
)


def input_main_field(layout: QVBoxLayout, label, placeholder):

    label_widget = QLabel(label)
    layout.addWidget(label_widget)

    input_entry = QLineEdit()
    input_entry.setPlaceholderText(placeholder)

    # 특정 위젯에만 스타일 적용을 위해 ObjectName 설정
    input_entry.setObjectName("main_user_inpt")

    layout.addWidget(input_entry)

    style = f"""
        #main_user_inpt {{ 
            color: black; 
            font-size: 14px; 
            background-color: {MAIN_WINDOW_BG_COLOR}; /* 배경색 변경 가능 */
            border: none; /* 전체 보더 제거 */
            border-bottom: 1px solid glay; /* 아래쪽 보더만 설정 */
        }}
        #main_user_inpt::placeholder {{ 
            color: gray; 
            font-style: italic; 
        }}
    """

    input_entry.setStyleSheet(style)

    return input_entry
