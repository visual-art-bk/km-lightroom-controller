import time
import ctypes
import pyautogui
from pywinauto import Application, keyboard
from state_manager.StateManager import StateManager
from .utils.get_lightroom_win import get_lightroom_win
from lightroom.utils.select_ui import select_ui
from PySide6.QtCore import QThread, Signal
from lightroom.set_template.set_template import set_template
from mornitorings.TaskManagerDetector import TaskManagerDetector
from helpers.log_exception_to_file import log_exception_to_file


def lock_mouse_keyboard():
    """✅ 마우스와 키보드 입력을 잠급니다 (Windows 전용)"""
    ctypes.windll.user32.BlockInput(True)  # 🔒 입력 차단
    pyautogui.FAILSAFE = False  # ⛔ 마우스 모서리 이동 방지


def unlock_mouse_keyboard():
    """✅ 마우스와 키보드 입력을 다시 활성화합니다"""
    ctypes.windll.user32.BlockInput(False)  # 🔓 입력 해제


class LightroomAutomationThread(QThread):
    """Lightroom 자동화 실행을 위한 스레드"""

    finished = Signal(bool)  # ✅ 성공/실패 여부를 전달하는 시그널
    failed = Signal(bool)

    def __init__(self):
        super().__init__()
        self.stop_flag = False  # ✅ 자동화 중지 플래그
        self.task_detector = TaskManagerDetector(
            self.stop_automation
        )  # ✅ 키 감지기 생성

    def stop_automation(self):
        """✅ `Ctrl + Alt + Delete` 감지 시 자동화 강제 중단"""
        print("❌ 자동화 강제 중단됨!")
        log_exception_to_file(exception_obj=None, message="작업관리자 실행으로 작업 강제 중단")
        self.stop_flag = True
        unlock_mouse_keyboard()  # ✅ 입력 차단 해제
        self.task_detector.stop()  # ✅ 키 감지 스레드 종료
        self.failed.emit(True)  # ❌ 자동화 실패 시그널 발생
        self.quit()

    def check_stop_flag(self, context=""):
        if self.stop_flag == True:
            print(f"⛔ 자동화 중단 감지! 실행 중지 {context}")
            self.failed.emit(True)
            unlock_mouse_keyboard()
            return self.stop_flag

    def run(self):
        lock_mouse_keyboard()

        self.task_detector.start()
        self.check_stop_flag()

        state_manager = StateManager()
        state = state_manager.get_state()

   
        app = Application(backend="uia").connect(
                title_re=".*Lightroom Classic.*", timeout=15
            )

        lightroom = app.window(title_re=".*Lightroom Classic.*")
        lightroom.wait("exists enabled visible ready", timeout=10)
        lightroom.wrapper_object().maximize()
        lightroom.wrapper_object().set_focus()

        self.check_stop_flag('공지 닫기: ESC 키 3회 입력')
        print("Lightroom 공지 닫기: ESC 키 3회 입력 시작...")
        for i in range(15):
            keyboard.send_keys("{ESC}")
            print(f"✅ ESC 키 입력 {i+1}/3 완료")
            time.sleep(0.1)
        print("✅ Lightroom 공지 닫기 완료!")

        try:
            self.check_stop_flag('파일(F) 메뉴 클릭')
            file_window = select_ui(
                control_type="MenuItem",
                title="파일(F)",
                win_specs=lightroom,
            )
            file_window.click_input()
            print("파일(F) 메뉴 클릭 완료!")

            self.check_stop_flag('연결전송된 촬영 메뉴 클릭')
            tet_capture_window = select_ui(
                win_specs=lightroom, control_type="MenuItem", title="연결전송된 촬영"
            )
            tet_capture_window.click_input()
            print("연결전송된 촬영 메뉴 클릭 완료!")

            self.check_stop_flag('연결전송된 촬영 시작... 클릭')
            start_tet_capture_window = select_ui(
                win_specs=lightroom,
                control_type="MenuItem",
                title="연결전송된 촬영 시작...",
            )
            start_tet_capture_window.click_input()
            print("연결전송된 촬영 시작 메뉴 클릭 완료!")

            self.check_stop_flag('세션 이름 입력')
            input_session_id_field = select_ui(
                win_specs=lightroom, title="세션 이름:", control_type="Edit"
            )

            input_session_id_field.set_text(f"{state.username}{state.phone_number}")
            print("사용자 이름과 전화번호 입력 완료!")

            self.check_stop_flag('템플릿 설정')
            set_template(win_spects=lightroom)

            #확인 버튼 클릭
            confirm_button = select_ui(
                win_specs=lightroom, title="확인", control_type="Button"
            )
            confirm_button.click_input()
            print("확인 버튼 클릭 완료!")

            state_manager.update_state(overlay_hide=True)
            print("✅ Lightroom 자동화 완료")

            self.finished.emit(True)
            unlock_mouse_keyboard()

        except Exception as e:
            print(f"❌ Lightroom 자동화 실패: {e}")
            self.failed.emit(True)
            log_exception_to_file(exception_obj=e, message="Lightroom 자동화 실패")
