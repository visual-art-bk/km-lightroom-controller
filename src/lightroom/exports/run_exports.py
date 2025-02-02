import time
from pywinauto.controls.uia_controls import ButtonWrapper
from pywinauto.keyboard import send_keys
from pywinauto import Application, WindowSpecification
from lightroom.tet_capture.selects.select_file_menu import select_file_menu
from lightroom.exports.selects.open_export_window import open_export_window
from lightroom.utils.select_ui import select_ui
from StateManager.StateManager import StateManager


def force_check_checkbox(window, checkbox_title):
    """✅ 특정 체크박스를 강제로 체크하는 함수"""
    try:
        checkbox = window.child_window(title=checkbox_title, control_type="CheckBox")

        if checkbox.exists(timeout=5):
            if not checkbox.get_toggle_state():
                checkbox.check()  # ✅ 강제 체크
                print(f"✅ '{checkbox_title}' 체크 완료!")
            else:
                print(f"🔘 '{checkbox_title}' 이미 체크되어 있음.")
        else:
            print(f"🚨 '{checkbox_title}' 체크박스를 찾을 수 없음!")

    except Exception as e:
        print(f"❌ 체크박스 체크 실패: {e}")


def run_exports(app: Application, lightroom: WindowSpecification):
    time.sleep(1)

    try:
        lightroom.set_focus()
        send_keys("^a")  # ✅ Ctrl + A 실행
        print("✅ Lightroom에서 전체 선택 완료!")

    except Exception as e:
        print(f"❌ Ctrl + A 실행 실패: {e}")

    state_manager = StateManager()

    app_state = state_manager.get_state()

    select_file_menu(app)

    export_window = open_export_window(lightroom=lightroom)

   
    chekbox_pushing_sub_folder = export_window.child_window(
            title="하위 폴더에 넣기:", control_type="CheckBox"
        )

    current_state = chekbox_pushing_sub_folder.legacy_properties()["Value"]
    
    if current_state != 1:
        print("체크박스 상태:", "✅ 체크됨" if current_state == 1 else "❌ 체크 안됨")
        chekbox_pushing_sub_folder.toggle()

    chekbox_pushing_sub_folder.toggle()

    edit_field = export_window.child_window(control_type="Edit", found_index=0)

    time.sleep(1)
    edit_field.set_text("")
    edit_field.set_text(f"{app_state.username}{app_state.phone_number}")

    export_button = export_window.child_window(
        title="내보내기", auto_id="1", control_type="Button"
    )
    time.sleep(1)
    export_button.click_input()

    pass
