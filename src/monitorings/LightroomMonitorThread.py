from PySide6.QtCore import QThread, Signal
from pywinauto import Application
import time
import psutil  # 프로세스 확인용

class LightroomMonitorThread(QThread):
    """Lightroom 종료 감지 스레드"""
    lightroom_closed = Signal()  # Lightroom 종료 시 신호 발생

    def run(self):
        """Lightroom이 종료될 때까지 감지"""
        while True:
            if not self.is_lightroom_running():
                print("!!!!!!!!!✅ Lightroom이 종료됨 - MainWindow 종료 신호 발생!!!!!!!!")
                self.lightroom_closed.emit()
                break
            time.sleep(1)  # 2초마다 상태 확인

    def is_lightroom_running(self):
        """Lightroom 프로세스가 실행 중인지 확인"""
        for process in psutil.process_iter(attrs=['name']):
            if "Lightroom.exe" in process.info['name']:  # Lightroom 프로세스명 확인
                return True
        return False
