import ctypes
import time
import pyautogui

def close_note_window():
    """불필요한 공지 창을 닫는 함수."""
    attempt = 0
    max_attempts = 10
    wait_time = 0.5
    
    while attempt < max_attempts:
        print(f"[INFO] 공지 창 닫기 시도 ({attempt + 1}/{max_attempts})")
        
        # ESC 키 전송
        pyautogui.press("esc")
        time.sleep(wait_time)
        
        # # ALT+F4 키 전송
        # pyautogui.hotkey("alt", "f4")
        # time.sleep(wait_time)
        
        attempt += 1
    
    # 최대 시도 후에도 닫히지 않으면 예외 발생
    error_message = "공지 창을 닫을 수 없습니다. 프로그램을 중지합니다."
    print(f"[ERROR] {error_message}")
    raise RuntimeError(error_message)
