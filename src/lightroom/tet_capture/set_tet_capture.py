import time
from pywinauto import WindowSpecification, keyboard
from lightroom import LightroomAutomationThread
from lightroom.utils import select_ui
from state_manager.StateManager import StateManager
from lightroom.set_template.set_template import set_template
from helpers.log_exception_to_file import log_exception_to_file
from pywinauto.findwindows import ElementNotFoundError

def click_file_menu(
    automation: LightroomAutomationThread, lightroom: WindowSpecification
):
    # 파일 메뉴 클릭
    automation.check_stop_flag("파일(F) 메뉴 클릭")
    
    attempt = 0
    max_attempts = 10
    wait_time = 0.5
    
    while attempt < max_attempts:
        try:
            file_window_with_close_note = lightroom.child_window(
                title="파일(F)", control_type="MenuItem"
            )
            
            if file_window_with_close_note.exists():
                file_window_with_close_note.click_input()
                return
            
        except ElementNotFoundError:
            log_exception_to_file.warning(f"파일(F) 메뉴를 찾을 수 없습니다. ({attempt + 1}/{max_attempts}) Esc 키 전송 시도")
            keyboard.send_keys("{ESC}")
            time.sleep(wait_time)
        
        attempt += 1
    
    # 최대 시도 후에도 실패하면 예외 발생
    error_message = "파일(F) 메뉴를 찾을 수 없습니다. 창을 닫고 프로그램을 다시 시작해주세요."
    log_exception_to_file.error(error_message)
    raise RuntimeError(error_message)


def click_tet_capture(
    automation: LightroomAutomationThread, lightroom: WindowSpecification
):
    automation.check_stop_flag("연결전송된 촬영 메뉴 클릭")
    tet_capture_window = select_ui(
        win_specs=lightroom, control_type="MenuItem", title="연결전송된 촬영"
    )
    tet_capture_window.click_input()


def set_tet_capture(
    automation: LightroomAutomationThread, lightroom: WindowSpecification
):
    state_manager = StateManager()
    state = state_manager.get_state()

    click_file_menu(automation=automation, lightroom=lightroom)

    click_tet_capture(automation=automation, lightroom=lightroom)

    stop_tet_capture_window = lightroom.child_window(
        title="연결전송된 촬영 중지",
        control_type="MenuItem",
    )

    if stop_tet_capture_window.exists():
        stop_tet_capture_window.click_input()

        # 연결전송된 촬영 중지 처음부터 다시
        click_file_menu(automation=automation, lightroom=lightroom)

    # 연결전송된 촬영 시작... 클릭
    automation.check_stop_flag("연결전송된 촬영 시작... 클릭")
    start_tet_capture_window = select_ui(
        win_specs=lightroom,
        control_type="MenuItem",
        title="연결전송된 촬영 시작...",
    )
    start_tet_capture_window.click_input()

    # 세션 이름 입력
    automation.check_stop_flag("세션 이름 입력")
    input_session_id_field = select_ui(
        win_specs=lightroom, title="세션 이름:", control_type="Edit"
    )
    input_session_id_field.set_text(f"{state.username}{state.phone_number}")

    # 템플릿 설정 자동화
    automation.check_stop_flag("템플릿 설정")
    set_template(win_spects=lightroom)

    # 확인 버튼 클릭
    confirm_button = select_ui(win_specs=lightroom, title="확인", control_type="Button")
    confirm_button.click_input()
    print("확인 버튼 클릭 완료!")
