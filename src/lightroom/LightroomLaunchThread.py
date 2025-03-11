from typedefs.signal_types import TypeSignalStatus
from constants.status_code import (
    LIGHTROOM_RUN_DETECTED,
    LIGHTROOM_RUN_FAILED,
    LIGHTROOM_EXCEPTION_RUN_FAILED,
)
import subprocess
import time
import psutil
from PySide6.QtCore import QThread, Signal
from constants import (
    SIGNAL_LIGHTROOM_LAUHCNER_START_FAILED,
    SIGNAL_LIGHTROOM_LAUHCNER_START_SUCCESS,
)
import logs

logger = logs.Logger()


class LightroomLaunchThread(QThread):
    """Lightroom 실행을 담당하는 스레드"""

    launch_start = Signal(dict)  # ✅ Lightroom 실행 완료 여부 신호

    def run(self):
        """Lightroom 실행 (부모 프로세스와 완전히 독립적으로 실행)"""
        print("🚀 Lightroom 실행 중...")

        try:
            # ✅ 부모 프로세스와 완전히 독립적으로 실행되도록 설정
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= (
                subprocess.STARTF_USESHOWWINDOW
            )  # 창을 숨기지 않도록 설정

            process = subprocess.Popen(
                [r"C:\Program Files\Adobe\Adobe Lightroom Classic\Lightroom.exe"],
                startupinfo=startupinfo,
                creationflags=subprocess.DETACHED_PROCESS
                | subprocess.CREATE_NEW_PROCESS_GROUP,  # ✅ 부모 프로세스와 완전히 독립적으로 실행
                close_fds=True,  # ✅ 부모 프로세스와 연결된 파일 디스크립터를 닫음
                shell=False,  # ✅ `False`로 설정하면 더 독립적으로 실행됨
            )

            # ✅ Lightroom 실행될 때까지 대기
            for _ in range(10):  # 최대 10초 대기
                if self.is_lightroom_running():
                    info: TypeSignalStatus = {
                        "message": "라이트룸 실행 성공",
                        "status": True,
                        "status_code": LIGHTROOM_RUN_DETECTED,
                    }
                    self.launch_start.emit(info)
                    logger.info(info)
                    return
                time.sleep(1)

            info: TypeSignalStatus = {
                "message": "Lightroom 실행 감지 실패",
                "status": False,
                "status_code": LIGHTROOM_RUN_FAILED,
            }
            self.launch_start.emit(info)
            logger.info(info)

        except Exception as e:
            info: TypeSignalStatus = {
                "message": "Lightroom 실행 실패",
                "status": False,
                "status_code": LIGHTROOM_EXCEPTION_RUN_FAILED,
            }
            self.launch_start.emit(info)
            logger.error(exception_obj=e, message=info)

    def is_lightroom_running(self):
        """Lightroom이 실행 중인지 확인"""
        for process in psutil.process_iter(attrs=["name"]):
            if "Lightroom.exe" in process.info["name"]:
                return True
        return False
