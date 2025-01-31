from pywinauto import Application
from ...utils.get_lightroom_win import get_lightroom_win

TITLE = "연결전송된 촬영"


def select_tet_capture(app: Application):
    try:
        print(f"[{TITLE}] 클릭 시작")

        lightroom = get_lightroom_win(app)

        tet_capture_menu = lightroom.child_window(title=TITLE, control_type="MenuItem")

        tet_capture_menu.wait(wait_for="exists enabled visible ready", timeout=60)

        tet_capture_menu.click_input()

        print(f"[{TITLE}] 클릭 성공")

    except Exception as e:
        is_exist = tet_capture_menu.exists(timeout=10)
        if is_exist == False:
            print(f"[{TITLE}] 메뉴가 존재하지 않음")

        print(f"[{TITLE}] 클릭 실패")
        print(e)
