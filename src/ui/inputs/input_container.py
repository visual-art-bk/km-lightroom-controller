from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QApplication,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QSizePolicy,
)


def createLabel(label: str):
    inputLabel = QLabel(label)
    inputLabel.setAlignment(Qt.AlignCenter)
    inputLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    inputLabel.setStyleSheet(
        """
        QLabel {
            color: #ffffff;
            font-size: 14px;
            font-weight: 600;
            border-radius: 16px;
            background-color: #426833; 
    }
    """
    )

    return inputLabel


def createEntry(placeholder: str):
    inputEntry = QLineEdit()
    inputEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    inputEntry.setPlaceholderText(f"  {placeholder}")
    inputEntry.setStyleSheet(
        """
            QLineEdit {
                border: none;
            }
            QLineEdit::placeholder {
                color: red;  /* 원하는 placeholder 텍스트 색상 */
            }
        """
    )

    return inputEntry


def createLayout(inputLabel: QLabel, inputEntry: QLineEdit):
    layout = QHBoxLayout()
    layout.addWidget(inputLabel, 1)
    layout.addWidget(inputEntry, 2)

    return layout


def input_container(label: str, placeholder: str):
    inputLabel = createLabel(label=label)
    inputEntry = createEntry(placeholder=placeholder)

    layout = createLayout(inputLabel=inputLabel, inputEntry=inputEntry)

    container = QWidget()
    container.setLayout(layout)
    container.setStyleSheet(
        """
            background-color: #EFF2E8;
            border-radius: 24px;
        """
    )
    container.setFixedSize(300, 50)

    return container
