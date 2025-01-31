import time
from pywinauto import Application, WindowSpecification
from ...utils.get_lightroom_win import get_lightroom_win

TITLE = "연결전송된 촬영 시작..."


def select_start_tet_capture(app: Application) -> WindowSpecification:
    try:
        print(f"[{TITLE}] 클릭 시작")

        lightroom = get_lightroom_win(app)

        start_tet_capture = lightroom.child_window(title=TITLE, control_type="MenuItem")

        start_tet_capture.wait(wait_for="exists enabled visible ready", timeout=60)

        is_exist = start_tet_capture.exists(timeout=10)
        print(f"[연결전송된 촬영 시작...] 존재 여부: {is_exist}")

        start_tet_capture.click_input()

        print(f"[{TITLE}] 클릭 성공")

        # tet_caputre_settings = lightroom.child_window(
        #     title="연결전송된 촬영 설정", control_type="Window"
        # )

        # is_exist = tet_caputre_settings.exists(timeout=10)
        # print(f"[연결전송된 촬영 설정] 존재 여부: {is_exist}")

        return start_tet_capture

    except Exception as e:
        is_exist = start_tet_capture.exists(timeout=10)
        if is_exist == False:
            print(f"[{TITLE}] 메뉴가 존재하지 않음")

        print(f"[{TITLE}] 클릭 실패")
        print(e)
