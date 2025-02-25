from typedefs.main_window_types import SizeDict
from PySide6.QtWidgets import (
    QWidget,
)


def create_central_widget(size: SizeDict):
    padding = 8
    width = size.get("width") - padding
    height = size.get("height") - padding

    x = padding // 2
    y = padding // 2

    widget = QWidget()

    widget.setGeometry(x, y, width, height)
    widget.setObjectName("centralWidget")

    style = """
        #centralWidget {
            background-color: #F9FFE2;
            border-radius: 32px;
        }
    """

    widget.setStyleSheet(style)

    return widget
