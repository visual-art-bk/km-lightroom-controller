from pywinauto import WindowSpecification
from pywinauto.controls.uia_controls import ComboBoxWrapper, ButtonWrapper


def check_no_detected_camera(selected_combo_text: str) -> bool:
    """선택된 콤보박스 값이 '카메라가 검색되지 않음'을 포함하는지 검사"""
    return "카메라가 검색되지 않음" in selected_combo_text


def search_camera(lightroom: WindowSpecification, get_user_state):
    state = get_user_state()

    userinfos_on_camera = lightroom.child_window(
        title=f"{ state.username}{state.phone_number}", control_type="Text"
    )

    try:
        parent_window = userinfos_on_camera.parent()
        children = parent_window.children()
        selected_combo_text = None

        for i, child in enumerate(children):
            if type(child) == ComboBoxWrapper:

                print("콤보박스 펼칩니다.")
                child.expand()

                import time

                print("창 펼친 채 1초대기")
                time.sleep(1)

                print("콤보박스 펼친 상태체크", child.get_expand_state())

                childern_of_combo = child.children()
                print(
                    i, "하위 자식들: ", childern_of_combo, " ComboBoxWrapper.children()"
                )

                for combo_child in childern_of_combo:
                    if type(combo_child) == ButtonWrapper:
                        print("콤보메뉴의 버튼 찾았습니다.")
                        print("버튼클릭")
                        combo_child.click()
                        img = child.capture_as_image()
                        img.save(f"콤보버튼클립캡쳐.jpg")
                        print("캡쳐완료")

                selected_combo_text = child.selected_text()
                print(f"선택된 콤보메뉴:", selected_combo_text)

        return selected_combo_text,
            

    except Exception as e:
        print("자식 요소 검사 중 예외발생", e)
