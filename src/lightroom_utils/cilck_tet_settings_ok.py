import time

def cilck_tet_settings_ok(settings):
    try:
        if settings == None:
            print('셋팅 값이 올바르지 않습니다.')
            return 
        
        print('셋팅값 입력중...')
        cancel_button = settings.child_window(title="OK", control_type="Button")
        cancel_button.wait("enabled", timeout=10)  # 버튼 활성화될 때까지 대기
        cancel_button.click_input()

        time.sleep(10)
   
    except Exception as e:
        print(f"OK 버튼 클릭 실패: {e}")