import time
from .utils.LightroomApp import LightroomApp
from .utils.get_lightroom_win import get_lightroom_win
from lightroom.utils.select_ui import select_ui
from StateManager.StateManager import StateManager
from PySide6.QtCore import QThread, Signal


class LightroomAutomationThread(QThread):
    """Lightroom 자동화 실행을 위한 스레드"""

    finished = Signal(bool)  # ✅ 성공/실패 여부를 전달하는 시그널

    def __init__(self):
        super().__init__()

    def run(self):
        state_manager = StateManager()
        state = state_manager.get_state()
        
        lightroomApp = LightroomApp()
        lightroomApp.start()

        app = lightroomApp.get_app()
        lightroom = get_lightroom_win(app)
        
        time.sleep(1.5)
        #  파일 메뉴 클릭
        file_window = select_ui(
            control_type="MenuItem",
            title="파일(F)",
            win_specs=lightroom,
        )
        file_window.click_input()

        #  연결전송된 촬영 메뉴 클릭
        tet_capture_window = select_ui(
            win_specs=lightroom, control_type="MenuItem", title="연결전송된 촬영"
        )
        tet_capture_window.click_input()

        #  연결전송된 촬영 시작 메뉴 클릭
        start_tet_capture_window = select_ui(
            win_specs=lightroom,
            control_type="MenuItem",
            title="연결전송된 촬영 시작...",
        )
        start_tet_capture_window.click_input()
        
        
        # 사용자 이름과 전화번호 입력
        input_session_id_field = select_ui(
            win_specs=lightroom,
            title='세션 이름:',
            control_type="Edit"
        )
        input_session_id_field.set_text("")
        input_session_id_field.set_text(f"{state.username}{state.phone_number}")
        
        
        # 확인 버튼 클릭
        confirm_button = select_ui(
            win_specs=lightroom,
            title='확인',
            control_type="Button"
        )
        confirm_button.click_input()
        
        state_manager.update_state(overlay_hide=True)

        self.finished.emit(True)


__all__ = ["init", "LightroomAutomationThread"]
