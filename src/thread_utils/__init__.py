import time
import threading
from gui_utils.overlay.OverlayWindow import OverlayWindow


def start_overlay_thread():
    """
    오버레이 창을 백그라운드에서 실행하는 스레드를 시작합니다.
    """
    print("오버레이 창을 백그라운드에서 실행하는 스레드를 시작합니다...")

    overlay_thread = threading.Thread(target=OverlayWindow.create_overlay, daemon=True)
    overlay_thread.start()

    time.sleep(5)  # 오버레이가 나타날 시간을 확보


__all__ = ["start_overlay_thread"]
