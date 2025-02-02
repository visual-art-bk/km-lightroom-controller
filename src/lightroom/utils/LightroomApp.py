import subprocess
import time
import psutil
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
from StateManager import StateManager


class LightroomApp:
    _instance = None  # Singleton 인스턴스 저장 변수
    state_manager = StateManager()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LightroomApp, cls).__new__(cls)
            cls._instance.app = None  # Pywinauto Application 객체
        return cls._instance

    def kill_lightroom(self):
        """Lightroom이 실행 중이라면 강제 종료"""
        for process in psutil.process_iter(attrs=["name", "pid"]):
            if "Lightroom.exe" in process.info["name"]:
                print(f"❌ Lightroom 프로세스 종료 중... (PID: {process.info['pid']})")
                process.terminate()  # 프로세스 종료 요청
                process.wait()  # 프로세스가 완전히 종료될 때까지 대기
                print("✅ Lightroom이 강제 종료되었습니다.")

    def restart(self):
        """무조건 Lightroom을 종료하고 새로 실행하는 메서드"""
        print("🔄 Lightroom을 재시작합니다...")

        # ✅ 기존 실행 중인 Lightroom 종료
        self.kill_lightroom()

        # ✅ Lightroom을 새로 실행
        print("🚀 Lightroom을 실행합니다...")
        subprocess.Popen(
            [r"C:\Program Files\Adobe\Adobe Lightroom Classic\Lightroom.exe"],
            creationflags=subprocess.DETACHED_PROCESS,  # Python 프로세스 종료와 무관하게 실행
        )

        time.sleep(10)  # Lightroom 실행을 위한 대기 시간
        print("✅ Lightroom 실행 완료!")

    def start(self):
        # self.restart()
        
        try:
            # ✅ 실행된 Lightroom과 연결
            self.app = Application(backend="uia").connect(
                path=r"C:\Program Files\Adobe\Adobe Lightroom Classic\Lightroom.exe",
                timeout=10,  # Lightroom 연결 시도
            )
            print("✅ pywinauto가 Lightroom에 성공적으로 연결됨!")

        except ElementNotFoundError:
            print("❌ Lightroom 연결 실패! 실행이 정상적으로 이루어졌는지 확인하세요.")
            self.app = None

    def get_app(self):
        """Lightroom 앱 객체를 반환"""
        if self.app is None:
            self.start()
        return self.app
