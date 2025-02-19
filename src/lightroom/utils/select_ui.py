import time
from pywinauto import WindowSpecification


def select_ui(
    win_specs: WindowSpecification, control_type, title, timeout=0.1
) -> WindowSpecification:
    try:
        child_window = win_specs.child_window(title=title, control_type=control_type)

        # ✅ 5초 동안 0.5초 간격으로 메뉴 확인 → 즉시 감지 가능
        for _ in range(10):
            if child_window.exists():

                return child_window
            time.sleep(timeout)

        raise RuntimeError(f"{title} 메뉴를 찾을 수 없습니다.")

    except Exception as e:
        print(f"❌ {title} 메뉴 클릭 실패: {e}")
