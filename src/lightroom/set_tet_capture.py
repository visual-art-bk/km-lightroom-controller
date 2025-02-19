from pywinauto import WindowSpecification
from lightroom import LightroomAutomationThread
from lightroom.utils import select_ui
from state_manager.StateManager import StateManager
from lightroom.set_template.set_template import set_template


def click_file_to_tet_capture(
    automation: LightroomAutomationThread, lightroom: WindowSpecification
):
    # 파일 메뉴 클릭
    automation.check_stop_flag("파일(F) 메뉴 클릭")
    file_window = select_ui(
        control_type="MenuItem",
        title="파일(F)",
        win_specs=lightroom,
    )
    file_window.click_input()

    # 파일 => 연결전송된 촬영 메뉴 클릭
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

    click_file_to_tet_capture(automation=automation, lightroom=lightroom)

    stop_tet_capture_window = lightroom.child_window(
        title="연결전송된 촬영 중지",
        control_type="MenuItem",
    )

    if stop_tet_capture_window.exists():
        stop_tet_capture_window.click_input()

        # 연결전송된 촬영 중지 처음부터 다시
        click_file_to_tet_capture(automation=automation, lightroom=lightroom)

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
