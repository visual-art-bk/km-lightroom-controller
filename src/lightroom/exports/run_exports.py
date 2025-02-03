import time
from pywinauto import Application, WindowSpecification
from lightroom.exports.selects.open_export_window import open_export_window
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


def toggle_checkbox(win_specs: WindowSpecification):
    current_state = get_state_legacy(win_specs=win_specs)
    if current_state != 1:
        print("체크박스 상태:", "✅ 체크됨" if current_state == 1 else "❌ 체크 안됨")
        win_specs.toggle()

    win_specs.toggle()


def open_export_path_dropdown(
    win_specs: WindowSpecification, item_name: str = "바탕 화면"
):
    # 1. '폴더:' 요소 찾기
    folder_label = win_specs.child_window(title="폴더:", control_type="Text")
    if not folder_label.exists():
        print("폴더 요소 찾지 못함!")
        return

    print("폴더 요소 찾았음")

    # 2. '폴더:' 요소의 부모 컨테이너(Pane) 찾기
    parent_pane = folder_label.parent()

    # 3. 부모 Pane에서 '내보낼 위치' ComboBox 찾기
    export_location_combo = None
    for element in parent_pane.descendants(control_type="ComboBox"):
        if element.rectangle().bottom < folder_label.rectangle().top:
            export_location_combo = element
            break  # 첫 번째 발견된 ComboBox 선택

    if not export_location_combo:
        print("내보낼 위치 ComboBox를 찾을 수 없습니다.")
        return


    
    from pywinauto.findwindows import ElementNotFoundError
    from pywinauto.controls.uia_controls import ComboBoxWrapper

    try:
        # 콤보박스에서 4번째 항목 선택
        export_location_combo.select('바탕 화면')
        print("선택 성공: 4번째 항목")

    except ElementNotFoundError:
        print("❌ 오류: ComboBox에서 4번째 항목을 찾을 수 없습니다. 요소가 존재하지 않습니다.")

    except AttributeError:
        print("❌ 오류: ComboBoxWrapper 객체가 아닙니다. 올바른 요소를 선택했는지 확인하세요.")

    except Exception as e:
        print(f"❌ 예기치 않은 오류 발생: {e}")

    # # 4. ComboBox 내부에서 '열기' 버튼 찾기
    # dropdown_button = next(
    #     (
    #         btn
    #         for btn in export_location_combo.children(control_type="Button")
    #         if btn.window_text() == "열기"
    #     ),
    #     None,
    # )

    # if not dropdown_button:
    #     print("열기 버튼을 찾을 수 없습니다.")
    #     return

    # print("열기 버튼 찾았음, 클릭 진행")
    # dropdown_button.click()  # '열기' 버튼 클릭하여 드롭다운 열기

    # print(dropdown_button)

    # time.sleep(3)

    # # 5. 드롭다운 리스트 찾기
    # dropdown_list = next(
    #     (lst for lst in export_location_combo.descendants(control_type="Pane")), None
    # )

    # if not dropdown_list:
    #     print("드롭다운 리스트를 찾을 수 없습니다.")

    # else:
    #     print("드롭다운 리스트를 찾았습니다.")

    # # # 6. 리스트 내부에서 원하는 항목("바탕화면") 찾기
    # # target_item = next(
    # #     (item for item in dropdown_list.children(control_type="ListItem") if item.window_text() == item_name),
    # #     None
    # # )

    # # if target_item:
    # #     print(f"'{item_name}' 선택 중...")
    # #     target_item.click_input()  # 리스트 항목 클릭
    # #     print(f"'{item_name}' 선택 완료!")
    # # else:
    # #     print(f"'{item_name}' 항목을 찾을 수 없습니다.")


def run_exports(app: Application, lightroom: WindowSpecification):
    state_manager = StateManager()
    app_state = state_manager.get_state()

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
    open_export_path_dropdown(win_specs=export_window)

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
