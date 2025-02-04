import subprocess
import time
import psutil
from PySide6.QtCore import QThread, Signal

class LightroomLaunchThread(QThread):
    """Lightroom 실행을 담당하는 스레드"""

    lightroom_started = Signal(bool)  # ✅ Lightroom 실행 완료 여부 신호

    def run(self):
        """Lightroom 실행 (부모 프로세스와 완전히 독립적으로 실행)"""
        print("🚀 Lightroom 실행 중...")

        try:
            # ✅ 부모 프로세스와 완전히 독립적으로 실행되도록 설정
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # 창을 숨기지 않도록 설정

            process = subprocess.Popen(
                [r"C:\Program Files\Adobe\Adobe Lightroom Classic\Lightroom.exe"],
                startupinfo=startupinfo,
                creationflags=subprocess.DETACHED_PROCESS
                | subprocess.CREATE_NEW_PROCESS_GROUP,  # ✅ 부모 프로세스와 완전히 독립적으로 실행
                close_fds=True,  # ✅ 부모 프로세스와 연결된 파일 디스크립터를 닫음
                shell=False,  # ✅ `False`로 설정하면 더 독립적으로 실행됨
            )

            # ✅ Lightroom 실행될 때까지 대기
            for _ in range(30):  # 최대 30초 대기
                if self.is_lightroom_running():
                    print("✅ Lightroom 실행 감지됨! (프로세스 유지)")
                    self.lightroom_started.emit(True)  # ✅ 실행 완료 시그널 발생
                    return
                time.sleep(1)

            print("❌ Lightroom 실행 감지 실패!")
            self.lightroom_started.emit(False)  # ❌ 실행 실패 시그널 발생

        except Exception as e:
            print(f"❌ Lightroom 실행 실패: {e}")
            self.lightroom_started.emit(False)  # ❌ 실행 실패 시그널 발생

    def is_lightroom_running(self):
        """Lightroom이 실행 중인지 확인"""
        for process in psutil.process_iter(attrs=["name"]):
            if "Lightroom.exe" in process.info["name"]:
                return True
        return False
