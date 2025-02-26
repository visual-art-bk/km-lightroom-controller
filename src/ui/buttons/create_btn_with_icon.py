from PySide6.QtWidgets import (
    QPushButton,
)

from PySide6.QtGui import QIcon, QCursor
from PySide6.QtCore import Qt, QSize


def create_btn_with_icon(width, height, icon_path) -> QPushButton:
    btn = QPushButton()
    btn.setIcon(QIcon(icon_path))
    btn.setIconSize(QSize(width, height))
    btn.setFixedSize(width, height)
    btn.setCursor(QCursor(Qt.PointingHandCursor))

    # ✅ 배경 제거 (투명한 버튼)
    btn.setStyleSheet(
        """
        QPushButton {
            background: transparent;
            border: none;
        }
        QPushButton:pressed {
            opacity: 0.7;  /* 버튼 클릭 시 약간 투명 효과 */
        }
    """
    )

    return btn
