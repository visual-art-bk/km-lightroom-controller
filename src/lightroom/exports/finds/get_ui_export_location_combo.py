from pywinauto import WindowSpecification
from pywinauto.controls.uia_controls import ComboBoxWrapper


def get_ui_export_location_combo(win_specs: WindowSpecification) -> ComboBoxWrapper:
    folder_label = win_specs.child_window(title="폴더:", control_type="Text")

    parent_pane = folder_label.parent()

    # 부모 Pane에서 '내보낼 위치' ComboBox 찾기
    export_location_combo = None
    for element in parent_pane.descendants(control_type="ComboBox"):
        if element.rectangle().bottom < folder_label.rectangle().top:
            export_location_combo = element
            break  # 첫 번째 발견된 ComboBox 선택

    if not export_location_combo:
        print("내보낼 위치 ComboBox를 찾을 수 없습니다.")
        return

    return export_location_combo