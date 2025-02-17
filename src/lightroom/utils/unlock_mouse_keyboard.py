import ctypes


def unlock_mouse_keyboard():
    """✅ 마우스와 키보드 입력을 다시 활성화합니다"""
    ctypes.windll.user32.BlockInput(False)
