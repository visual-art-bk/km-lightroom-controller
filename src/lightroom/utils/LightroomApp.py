from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
import time


class LightroomApp:
    _instance = None  # Singleton 인스턴스 저장 변수

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LightroomApp, cls).__new__(cls)
            cls._instance.app = None  # Pywinauto Application 객체
            cls._instance.lightroom = None  # Lightroom 메인 창 객체
        return cls._instance

    def start(self):
        if self.app is None:
            print("Lightroom Classic 실행 중...")

            self.app = Application(backend="uia").start(
                r"C:\Program Files\Adobe\Adobe Lightroom Classic\Lightroom.exe"
            )

    def get_app(self):
        if self.app is None:
            self.start()
        return self.app
