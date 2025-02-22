import time
from pywinauto import keyboard


def send_esc_key(parent):
    parent.check_stop_flag("공지 닫기: ESC 키 3회 입력")

    print("Lightroom 공지 닫기: ESC 키 3회 입력 시작...")

    for i in range(15):
        keyboard.send_keys("{ESC}")
        time.sleep(0.1)

    print("✅ Lightroom 공지 닫기 시도 완료")
