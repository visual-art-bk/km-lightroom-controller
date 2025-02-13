from PySide6.QtWidgets import (
    QGridLayout,
)
from PySide6.QtCore import Qt
from ui.content_layout.TextContainerWidget import TextContainerWidget
from ui.content_layout.text_contents import text_contents


def content_layout(height):
    text_container = TextContainerWidget(
        text_contents=text_contents,
        font_sizes=20,
        text_color="black",
        height=height,
    )

    layout = QGridLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignCenter)
    layout.addWidget(text_container, 0, 0, Qt.AlignCenter)

    return layout
