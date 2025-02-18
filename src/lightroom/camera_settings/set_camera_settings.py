from pywinauto import WindowSpecification
from pywinauto.base_wrapper import BaseWrapper
from pywinauto.controls.uia_controls import ComboBoxWrapper


def check_static_label(child: BaseWrapper, label):
    texts = child.texts()

    is_matched_with_label = False
    for tex in texts:
        if tex == label:
            is_matched_with_label = True
            break
    return is_matched_with_label


def search_settings(parent_window: BaseWrapper, title, config_setting):
    try:
        children = parent_window.children()

        for i, child in enumerate(children):
            child: BaseWrapper

            if type(child) == ComboBoxWrapper:
                static_label_to_check = children[i - 1]

                if check_static_label(child=static_label_to_check, label=title):
                    print(f"{title} 라벨 찾았습니다. 자동화시작")

                    child.select(config_setting)

    except Exception as e:
        print(title, "카메라 세팅 탐색 중 에러 발생", e)


def set_camera_settings(
    lightroom: WindowSpecification, title, control_type, config_setting
):
    """카메라의 iso 조리개등의 옵션을 세팅한다"""

    iso_label = lightroom.child_window(title=title, control_type=control_type)

    if iso_label.exists():

        parent_window = iso_label.parent()

        search_settings(parent_window, title=title, config_setting=config_setting)
    else:
        print("iso 세팅이 존재하지 않습니다.")
