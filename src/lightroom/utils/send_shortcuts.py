from pywinauto.keyboard import send_keys
from pywinauto import WindowSpecification


def send_shortcuts(win_specs: WindowSpecification, keys, context="정의되지않음"):
    if not keys:
        raise ValueError(f"키보드에서 전송할 keys값은 반드시 필요. 현재 keys: {keys}")
    try:
        win_specs.set_focus()
        send_keys(keys)  # ✅ Ctrl + A 실행
        print(f"✅ {context} - 키값 {keys} 전송 성공")

    except Exception as e:
        print(f"❌ {context} - 키값 {keys} 전송 실패 {e}")
