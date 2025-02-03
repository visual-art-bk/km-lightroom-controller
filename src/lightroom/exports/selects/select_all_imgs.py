from pywinauto import WindowSpecification
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.controls.uia_controls import ComboBoxWrapper
from typing import Optional, List, Tuple


def find_window_by_keywords(win_specs: WindowSpecification, keywords: list) -> Optional[WindowSpecification]:
    """ 키워드 기반으로 첫 번째 매칭되는 Pane 찾기 """
    for keyword in keywords:
        try:
            element = win_specs.child_window(title_re=keyword, auto_id="65535", control_type="Pane")
            if element.exists():
                print(f"✅ 매칭 성공! - 찾은 창: {keyword} - {element.window_text()}")
                return element

        except ElementNotFoundError:
            print(f"❌ '{keyword}' 요소를 찾을 수 없습니다. 다음 키워드로 넘어갑니다.")
            continue  # 다음 키워드 탐색

        except Exception as e:
            print(f"⚠️ 예기치 않은 오류 발생: {e}")
            continue  # 기타 오류도 안전하게 처리

    print("🚫 어떤 창도 매칭되지 않았습니다.")
    return None


def get_all_controls_from_pane(pane: WindowSpecification) -> List[Tuple[str, WindowSpecification]]:
    """
    `Pane` 내부의 모든 UI 컨트롤을 탐색하여 반환
    :param pane: 검색할 UI Pane
    :return: (control_type, WindowSpecification) 리스트
    """
    found_controls = []  # 찾은 컨트롤 저장 리스트

    try:
        for element in pane.descendants():
            control_type = element.friendly_class_name()  # 컨트롤 타입 가져오기
            print(f"🔍 찾은 컨트롤: {control_type} - {element}")
            found_controls.append((control_type, element))  # (control_type, element) 튜플로 저장

    except Exception as e:
        print(f"⚠️ UI 컨트롤 찾기 실패: {e}")

    return found_controls  # 찾은 모든 요소 리스트 반환


def get_ui_element_by_type(pane: WindowSpecification, target_type: str) -> Optional[WindowSpecification]:
    """
    `Pane` 내부에서 특정 `control_type`을 가진 UI 요소 찾기
    :param pane: 검색할 UI Pane
    :param target_type: 찾고자 하는 UI 요소 타입 (예: 'ComboBox', 'Button', 'Edit' 등)
    :return: 첫 번째로 발견된 해당 타입의 UI 요소 반환 (없으면 None)
    """
    try:
        for element in pane.descendants():
            control_type = element.friendly_class_name()
            if control_type == target_type:
                print(f"✅ {target_type} 찾음: {element}")
                return element  # 첫 번째로 발견된 해당 타입의 요소 반환
    except Exception as e:
        print(f"⚠️ {target_type} 찾기 실패: {e}")

    print(f"🚫 {target_type} 요소를 찾을 수 없습니다.")
    return None  # 찾지 못하면 None 반환


def click_and_get_controls(pane: WindowSpecification) -> Optional[List[Tuple[str, WindowSpecification]]]:
    """
    `Pane`을 클릭한 후 내부의 모든 컨트롤을 검색하여 반환
    :param pane: 클릭할 UI Pane
    :return: 내부의 모든 UI 컨트롤 리스트 (없으면 None)
    """
    try:
        if pane.exists():
            pane.click_input()
            print(f"✅ 클릭 성공: {pane}")
            return get_all_controls_from_pane(pane)
        else:
            print("❌ 클릭할 요소가 존재하지 않습니다.")
            return None
    except Exception as e:
        print(f"⚠️ 클릭 중 오류 발생: {e}")
        return None


def select_all_imgs(win_specs: WindowSpecification) -> Optional[ComboBoxWrapper]:
    """ '이전 가져오기' 또는 '모든 사진' 창을 찾아 ComboBox 반환 """
    keywords = [r"이전 가져오기.*", r"모든 사진.*"]

    # 1️⃣ 키워드 기반으로 창 찾기
    get_imgs = find_window_by_keywords(win_specs, keywords)
    if not get_imgs:
        return None  # 창을 찾지 못하면 종료

    # 2️⃣ 창을 클릭하고 내부 UI 컨트롤 검색
    controls = click_and_get_controls(get_imgs)
    if not controls:
        return None

    # 3️⃣ `Pane` 내부에서 `ComboBox` 찾기
    export_location_combo = get_ui_element_by_type(get_imgs, "ComboBox")

    if export_location_combo:
        print(f"✅ ComboBox 찾음: {export_location_combo}")
    else:
        print("❌ ComboBox를 찾을 수 없습니다.")

    return export_location_combo
