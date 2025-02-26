from typedefs.main_window_types import SizeDict
from PySide6.QtWidgets import (
    QWidget,
)


def create_main_display_widget(size: SizeDict):
    width = size.get("width")
    height = size.get("height")

    style = """
            background-color: yellow;
        """
    display = QWidget()

    display.setStyleSheet(style)
    display.setFixedSize(width, height)
    
    return display

