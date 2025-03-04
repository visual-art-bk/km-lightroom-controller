import time
from helpers.config_loader import load_config
from constants import (
    SIGNAL_NO_DETECTED_CAMERA,
    SIGNAL_NO_SEARCHED_CAMERA,
    NO_DETECTED_CAMERA_NAME,
    SIGNAL_LIGHTROOM_AUTOMATION_FOCUS_FAILED,
    SIGNAL_LIGHTROOM_AUTOMATION_CONTROL_FAILED,
    SIGNAL_LIGHTROOM_AUTOMATION_CONNECT_FAILED,
)

from pywinauto import Application, keyboard
from state_manager.StateManager import StateManager
from lightroom.utils.select_ui import select_ui
from PySide6.QtCore import QThread, Signal

from mornitorings.TaskManagerDetector import TaskManagerDetector
from helpers.log_exception_to_file import log_exception_to_file
from lightroom.note_window_handlers.send_esc_key import send_esc_key
from lightroom.note_window_handlers.close_note_window import close_note_window
from lightroom.check_camera_state import detect_camera, search_camera
from lightroom.utils import lock_mouse_keyboard, unlock_mouse_keyboard
from lightroom.tet_capture.set_tet_capture import set_tet_capture
from lightroom.camera_settings import set_camera_settings

config = load_config()
ISO_SETTING = config.get("ISO")
WB_SETTING = config.get("WB")
SHUTTER_SETTING = config.get("셔터")
APERTURE_SETTING = config.get("조리개")

TIMEOUT_CONNECT_LIGHTROOM = 5
TIMEOUT_WAIT_LIGHTROOM_VISIBLE = 5


class LightroomAutomationThread(QThread):
    """Lightroom 자동화 실행을 위한 스레드"""

    finished = Signal(bool)  # ✅ 성공/실패 여부를 전달하는 시그널
    failed = Signal(str)

    def __init__(self):
        super().__init__()
        self.stop_flag = False  # ✅ 자동화 중지 플래그
        self.task_detector = TaskManagerDetector(
            self.stop_automation
        )  # ✅ 키 감지기 생성

    def run(self):
        lock_mouse_keyboard()

        self.task_detector.start()
        self.check_stop_flag()

        state_manager = StateManager()

        try:
            app = Application(backend="uia").connect(
                title_re=".*Lightroom Classic.*", timeout=TIMEOUT_CONNECT_LIGHTROOM
            )
        except Exception as e:
            log_exception_to_file(exception_obj=e, message="라이트룸 연결 실패")
            self.failed.emit(SIGNAL_LIGHTROOM_AUTOMATION_CONNECT_FAILED)
            unlock_mouse_keyboard()
            return

        try:
            send_esc_key(parent=self)
            
            lightroom = app.window(title_re=".*Lightroom Classic.*")
            lightroom.wait(
                "exists enabled visible ready", timeout=TIMEOUT_WAIT_LIGHTROOM_VISIBLE
            )
            lightroom.wrapper_object().maximize()
            lightroom.wrapper_object().set_focus()

            

        except Exception as e:
            log_exception_to_file(
                exception_obj=e,
                message="라이트룸 연결 후, 윈도우 탐색 실패, 포커스를 맞추지 못함, 모든 공지 창을 닫아야함",
            )
            self.failed.emit(SIGNAL_LIGHTROOM_AUTOMATION_FOCUS_FAILED)
            unlock_mouse_keyboard()
            return

        try:
            set_tet_capture(automation=self, lightroom=lightroom)

            # 너무 빠른 카메라 감지 체크를 하면
            # 카메라가 올바르게 연결되어있음에도
            # 카메라 감지 실패할 수 있으니 딜레이를 준다.
            time.sleep(1.5)

            have_detected_camera = detect_camera(lightroom=lightroom)
            if not have_detected_camera:
                self.failed.emit(SIGNAL_NO_DETECTED_CAMERA)
                return

            camer_name = search_camera(
                lightroom=lightroom, get_user_state=state_manager.get_state
            )

            if NO_DETECTED_CAMERA_NAME in camer_name:
                self.failed.emit(SIGNAL_NO_SEARCHED_CAMERA)
                return

            # SHUTTER 세팅
            set_camera_settings(
                lightroom=lightroom,
                title="셔터:",
                control_type="Text",
                config_setting=SHUTTER_SETTING,
            )

            # 조리개 세팅
            set_camera_settings(
                lightroom=lightroom,
                title="조리개:",
                control_type="Text",
                config_setting=APERTURE_SETTING,
            )

            # ISO 세팅
            set_camera_settings(
                lightroom=lightroom,
                title="ISO:",
                control_type="Text",
                config_setting=ISO_SETTING,
            )

            # WB 세팅
            set_camera_settings(
                lightroom=lightroom,
                title="WB:",
                control_type="Text",
                config_setting=WB_SETTING,
            )

            print("✅ Lightroom 자동화 완료")
            self.finished.emit(True)

        except Exception as e:
            print(f"❌ Lightroom 자동화 실패: {e}")
            self.failed.emit(SIGNAL_LIGHTROOM_AUTOMATION_CONTROL_FAILED)
            log_exception_to_file(exception_obj=e, message="Lightroom 자동화 실패")
        finally:
            unlock_mouse_keyboard()

    def stop_automation(self):
        """✅ `Ctrl + Alt + Delete` 감지 시 자동화 강제 중단"""
        print("❌ 자동화 강제 중단됨!")
        log_exception_to_file(
            exception_obj=None, message="작업관리자 실행으로 작업 강제 중단"
        )
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
