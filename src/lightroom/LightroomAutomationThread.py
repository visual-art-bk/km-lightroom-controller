import time
import psutil
from pywinauto import Application
from state_manager.StateManager import StateManager
from .utils.get_lightroom_win import get_lightroom_win
from lightroom.utils.select_ui import select_ui
from PySide6.QtCore import QThread, Signal


class LightroomAutomationThread(QThread):
    """Lightroom 자동화 실행을 위한 스레드"""

    finished = Signal(bool)  # ✅ 성공/실패 여부를 전달하는 시그널

    def __init__(self):
        super().__init__()

    def run(self):
        state_manager = StateManager()
        state = state_manager.get_state()

        # ✅ Lightroom 프로세스에 직접 연결
        try:
            app = Application(backend="uia").connect(
                path=r"C:\Program Files\Adobe\Adobe Lightroom Classic\Lightroom.exe",
                timeout=15,  # Lightroom 연결 시도 (최대 15초 대기)
            )
            print("✅ Lightroom에 성공적으로 연결됨!")
        except Exception as e:
            print(f"❌ Lightroom 연결 실패: {e}")
            self.finished.emit(False)  # ❌ 연결 실패 시그널 발생
            return

        # ✅ Lightroom 창 가져오기
        lightroom = get_lightroom_win(app)

        time.sleep(2)

        try:
            # ✅ 파일 메뉴 클릭
            file_window = select_ui(
                control_type="MenuItem",
                title="파일(F)",
                win_specs=lightroom,
            )
            file_window.click_input()

            # ✅ 연결전송된 촬영 메뉴 클릭
            tet_capture_window = select_ui(
                win_specs=lightroom, control_type="MenuItem", title="연결전송된 촬영"
            )
            tet_capture_window.click_input()

            # ✅ 연결전송된 촬영 시작 메뉴 클릭
            start_tet_capture_window = select_ui(
                win_specs=lightroom,
                control_type="MenuItem",
                title="연결전송된 촬영 시작...",
            )
            start_tet_capture_window.click_input()

            # ✅ 사용자 이름과 전화번호 입력
            input_session_id_field = select_ui(
                win_specs=lightroom,
                title="세션 이름:",
                control_type="Edit"
            )
            input_session_id_field.set_text("")
            input_session_id_field.set_text(f"{state.username}{state.phone_number}")

            # ✅ 확인 버튼 클릭
            confirm_button = select_ui(
                win_specs=lightroom,
                title="확인",
                control_type="Button"
            )
            confirm_button.click_input()

            state_manager.update_state(overlay_hide=True)

            print("✅ Lightroom 자동화 완료")
            self.finished.emit(True)  # ✅ 자동화 성공 시그널 발생

        except Exception as e:
            print(f"❌ Lightroom 자동화 실패: {e}")
            self.finished.emit(False)  # ❌ 자동화 실패 시그널 발생
