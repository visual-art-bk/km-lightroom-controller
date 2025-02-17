import ctypes
import pyautogui


def lock_mouse_keyboard():
    """✅ 마우스와 키보드 입력을 잠급니다 (Windows 전용)"""
    ctypes.windll.user32.BlockInput(True)  # 🔒 입력 차단
    pyautogui.FAILSAFE = False  # ⛔ 마우스 모서리 이동 방지
