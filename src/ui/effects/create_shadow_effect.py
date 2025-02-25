from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

def create_shadow_effect():
    shadow = QGraphicsDropShadowEffect()

    shadow.setBlurRadius(30)
    shadow.setYOffset(6)
    shadow.setColor(QColor(0, 0, 0, 120))


    return shadow