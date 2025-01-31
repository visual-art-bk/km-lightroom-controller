from pywinauto import Application
from ..get_lightroom_win import get_lightroom_win


def select_tet_capture(app: Application):
    try:
        print("Tethered Capture 클릭 시작...")

        lightroom = get_lightroom_win(app)

        tet_capture_menu = lightroom.child_window(title="Tethered Capture", control_type="MenuItem")

        tet_capture_menu.wait(wait_for="exists enabled visible ready", timeout=60)

        tet_capture_menu.click_input()

        print("Tethered Capture 클릭 성공")

        tet_capture_menu.child_window().print_control_identifiers()

    except Exception as e:
        is_exist = tet_capture_menu.exists(timeout=10)
        if is_exist == False:
            print("Tethered Capture 메뉴 존재하지 않음")

        print(f"Tethered Capture 메뉴 클릭 실패: {e}")
