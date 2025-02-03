import time
from pywinauto import Application, WindowSpecification
from lightroom.exports.selects.open_export_window import open_export_window
from lightroom.exports.selects.select_all_imgs import select_all_imgs
from lightroom.exports.finds.get_ui_export_location_combo import (
    get_ui_export_location_combo,
)
from lightroom.utils.select_ui import select_ui
from lightroom.utils.send_shortcuts import send_shortcuts
from lightroom.utils.get_state_legacy import get_state_legacy
from StateManager.StateManager import StateManager

KEYS_SELECT_ALL = "^a"
KEYS_SELECT_EXPORT = "^+E"
CONTROL_TYPE_FILE_MENU = "MenuItem"
CONTROL_TYPE_CHECKBOX = "CheckBox"
CONTROL_TYPE_EXPORT_PATH = "Button"
TITLE_FILE_MENU = "파일(F)"
TITLE_SUB_FOLDER = "하위 폴더에 넣기:"
TITLE_EXPORT_PATH = "열기"
TEXT_DESKTOP = "바탕 화면"


def toggle_checkbox(win_specs: WindowSpecification):
    current_state = get_state_legacy(win_specs=win_specs)
    if current_state != 1:
        print("체크박스 상태:", "✅ 체크됨" if current_state == 1 else "❌ 체크 안됨")
        win_specs.toggle()
        return


def run_exports(lightroom: WindowSpecification):
    state_manager = StateManager()
    app_state = state_manager.get_state()

    # TODO    
    # select_all_imgs(win_specs=lightroom)

    # 전체 사진 단축키로 선택
    send_shortcuts(
        keys=KEYS_SELECT_ALL,
        context="전체 사진 선택 Ctrl + A 실행",
        win_specs=lightroom,
    )

    # 파일 메뉴 열기
    select_ui(
        control_type=CONTROL_TYPE_FILE_MENU,
        title=TITLE_FILE_MENU,
        win_specs=lightroom,
    )

    # 내보내기 단축키로 누르기
    send_shortcuts(
        keys=KEYS_SELECT_EXPORT,
        context=f"내보내기 단축키 {KEYS_SELECT_EXPORT}",
        win_specs=lightroom,
    )

    # 내보내기 단축키로 활성화
    export_window = open_export_window(lightroom=lightroom)

    # 내보내기 위치 자동화
    ui_export_location_combo = get_ui_export_location_combo(win_specs=export_window)
    # 위치 콤보박스에서 바탕화면 선택
    ui_export_location_combo.select(TEXT_DESKTOP)

    # 하위 폴더에 넣기 요소
    checkbox_sub_folder = select_ui(
        control_type=CONTROL_TYPE_CHECKBOX,
        title=TITLE_SUB_FOLDER,
        win_specs=export_window,
    )

    # 하위 폴더 넣기 체크박스
    toggle_checkbox(win_specs=checkbox_sub_folder)

    edit_field = export_window.child_window(control_type="Edit", found_index=0)

    time.sleep(1)
    edit_field.set_text("")
    edit_field.set_text(f"{app_state.username}{app_state.phone_number}")

    export_button = export_window.child_window(
        title="내보내기", auto_id="1", control_type="Button"
    )
    time.sleep(1)
    export_button.click_input()
