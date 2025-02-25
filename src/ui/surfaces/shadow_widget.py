from typedefs.main_window_types import SizeDict
from PySide6.QtWidgets import QWidget


def create_shadow_widget(size: SizeDict):
    width = size.get("width")
    height = size.get("height")

    shadowWidget = QWidget()
    shadowWidget.setGeometry(0, 0, width, height)

    style = """
            background-color: #BFBFBF;  /* 연한 회색 배경 */
            border-radius: 36px;
        """

    shadowWidget.setStyleSheet(style)

    return shadowWidget
