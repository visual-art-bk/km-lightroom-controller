from PySide6.QtCore import QThread, Signal
import time
import psutil  # 프로세스 확인용


class LightroomMonitorThread(QThread):
    """Lightroom 실행 감지 및 종료 감지 스레드"""

    lightroom_closed_mornitoring = Signal()  # ✅ Lightroom 종료 시그널

    def run(self):
        """Lightroom이 종료될 때까지 감지"""
        while True:
            if not self.is_lightroom_running():
                print("✅ Lightroom 종료 감지됨 → 프로그램 종료")
                self.lightroom_closed_mornitoring.emit()  # ✅ Lightroom 종료 시그널 발생
                break
            time.sleep(0.5)  # 0.5초마다 Lightroom 상태 확인

    def is_lightroom_running(self):
        """Lightroom이 실행 중인지 확인"""
        for process in psutil.process_iter(attrs=["name"]):
            if "Lightroom.exe" in process.info["name"]:
                return True
        return False
