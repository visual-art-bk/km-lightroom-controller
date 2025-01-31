import time
from pywinauto import Application
from ..get_lightroom_win import get_lightroom_win


def select_file_menu(app: Application):
    try:
        lightroom = get_lightroom_win(app)

        print('File 메뉴 클릭 시작..')
        
        time.sleep(5)

        file_menu = lightroom.child_window(title="File", control_type="MenuItem")

        file_menu.wait(wait_for="exists enabled visible ready", timeout=60)

        file_menu.click_input()

        print('File 메뉴 클릭 성공')
    except Exception as e:
        is_exist = file_menu.exists(timeout=10)
        if is_exist == False:
            print("파일 메뉴 존재하지 않음")

        print(f"File 메뉴 클릭 실패: {e}")
