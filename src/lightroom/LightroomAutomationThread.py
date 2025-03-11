import helpers
import time
from typedefs.signal_types import TypeAutomationSignal, TypeSignalStatus
from helpers.config_loader import load_config
from constants.status_code import (
    AUTOMATION_APPLICATOIN_INIT_FAILED,
    AUTOMATION_LIGHTROOM_WINDOW_NOT_FOUNT,
    AUTOMATION_EXCEPTION_FAILED,
    CAMERA_NOT_DETECTED,
    CAMERA_NOT_SEARCHED,
)
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
import logs

logger = logs.Logger()

config = load_config()
ISO_SETTING = config.get("ISO")
WB_SETTING = config.get("WB")
SHUTTER_SETTING = config.get("셔터")
APERTURE_SETTING = config.get("조리개")

TIMEOUT_CONNECT_LIGHTROOM = 5
TIMEOUT_WAIT_LIGHTROOM_VISIBLE = 5


class LightroomAutomationThread(QThread):
    """Lightroom 자동화 실행을 위한 스레드"""

    automation = Signal(dict)
    automation_steps = Signal(dict)

    def _on_automation_steps(self, info: TypeAutomationSignal):
        helpers.log_exception_to_file(message=info["message"])

        if info["status"] is False:
            lock_mouse_keyboard()
            unlock_mouse_keyboard()
            self.automation.emit(info)

    def __init__(self):
        super().__init__()
        self.stop_flag = False  # ✅ 자동화 중지 플래그
        self.task_detector = TaskManagerDetector(
            self.stop_automation
        )  # ✅ 키 감지기 생성

        self.automation_steps.connect(self._on_automation_steps)

    def run(self):
        lock_mouse_keyboard()

        self.task_detector.start()
        self.check_stop_flag()

        state_manager = StateManager()

        try:
            app = Application(backend="uia").connect(
                title_re=".*Lightroom Classic.*", timeout=5
            )
        except Exception as e:
            unlock_mouse_keyboard()
            info: TypeSignalStatus = {
                "status_code": AUTOMATION_APPLICATOIN_INIT_FAILED,
                "message": "라이트룸 어플리케이션 초기화 실패했습니다.",
                "status": False,
            }

            self.automation.emit(info)
            logger.error(exception_obj=e, message=info)
            return

        try:
            send_esc_key(parent=self)

            lightroom = app.window(title_re=".*Lightroom Classic.*")
            lightroom.wait("exists enabled visible ready", timeout=5)
            lightroom.wrapper_object().maximize()
            lightroom.wrapper_object().set_focus()

        except Exception as e:
            unlock_mouse_keyboard()
            info: TypeSignalStatus = {
                "status_code": AUTOMATION_LIGHTROOM_WINDOW_NOT_FOUNT,
                "message": "라이트룸 연결후, 윈도우 찾기 실패했습니다.",
                "status": False,
            }

            self.automation.emit(info)
            logger.error(exception_obj=e, message=info)
            return

        try:
            set_tet_capture(
                automation=self, lightroom=lightroom, signal=self.automation_steps
            )

            # 너무 빠른 카메라 감지 체크를 하면
            # 카메라가 올바르게 연결되어있음에도
            # 카메라 감지 실패할 수 있으니 딜레이를 준다.
            time.sleep(1.5)

            have_detected_camera = detect_camera(lightroom=lightroom)
            if not have_detected_camera:
                unlock_mouse_keyboard()
                info: TypeAutomationSignal = {
                    "status_code": CAMERA_NOT_DETECTED,
                    "message": "카메라를 감지하지 못햇습니다.",
                    "status": False,
                }
                self.automation.emit(info)
                logger.info(info)
                return

            camer_name = search_camera(
                lightroom=lightroom, get_user_state=state_manager.get_state
            )

            if NO_DETECTED_CAMERA_NAME in camer_name:
                unlock_mouse_keyboard()

                info: TypeAutomationSignal = {
                    "status_code": CAMERA_NOT_SEARCHED,
                    "message": "카메라가 검색되지 않았습니다.",
                    "status": False,
                }
                self.automation.emit(info)
                logger.info(info)
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

            info: TypeSignalStatus = {
                "error_code": "",
                "message": "Lightroom 자동화 완료",
                "status": True,
            }
            self.automation.emit(info)
            unlock_mouse_keyboard()

        except Exception as e:
            unlock_mouse_keyboard()
            info: TypeSignalStatus = {
                "status_code": AUTOMATION_EXCEPTION_FAILED,
                "message": "Lightroom 자동화가 예외발생으로 실패했습니다.",
                "status": False,
            }
            self.automation.emit(info)
            logger.error(exception_obj=e, message=info)

    def stop_automation(self):
        """✅ `Ctrl + Alt + Delete` 감지 시 자동화 강제 중단"""
        m = "작업관리자 실행으로 작업 강제 중단되었습니다."
        log_exception_to_file(exception_obj=None, message=m)
        self.stop_flag = True
        unlock_mouse_keyboard()  # ✅ 입력 차단 해제

        self.task_detector.stop()  # ✅ 키 감지 스레드 종료

        info: TypeAutomationSignal = {"error_code": "", "message": m, "status": False}
        self.automation.emit(info)  # ❌ 자동화 실패 시그널 발생
        self.quit()

    def check_stop_flag(self, context=""):
        if self.stop_flag == True:

            m = "작업관리자 실행으로 작업 강제 중단되었습니다."
            log_exception_to_file(exception_obj=None, message=m)
            info: TypeAutomationSignal = {
                "error_code": "",
                "message": m,
                "status": False,
            }
            self.automation.emit(info)
            unlock_mouse_keyboard()
            return self.stop_flag
