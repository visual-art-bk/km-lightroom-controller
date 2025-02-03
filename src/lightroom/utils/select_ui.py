import time
from pywinauto import WindowSpecification


def select_ui(
    win_specs: WindowSpecification,
    title="정의되지않음",
    control_type="정의되지않음",
    timeout=0.1,
) -> WindowSpecification:
    try:
        print(f"{title} 메뉴 클릭 시작..")

        ui = win_specs.child_window(title=title, control_type=control_type)

        # ✅ 5초 동안 0.5초 간격으로 메뉴 확인 → 즉시 감지 가능
        for _ in range(10):
            if ui.exists():
                ui.click_input()
                print(f"{title}  메뉴 클릭 성공!")
                return ui
            time.sleep(timeout)

        print(f"🚨 {title}  메뉴가 존재하지 않음!")
        raise RuntimeError(f"{title}  메뉴를 찾을 수 없습니다.")

    except Exception as e:
        print(f"❌{title}  메뉴 클릭 실패: {e}")
