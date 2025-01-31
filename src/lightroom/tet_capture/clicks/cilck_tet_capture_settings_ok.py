from pywinauto import WindowSpecification

TITLE = '확인'

def cilck_tet_capture_settings_ok(win_specs: WindowSpecification):
    print(f"[{TITLE}] 버튼 클릭 시작")
    
    try:
        ok_button = win_specs.child_window(
            title=TITLE, control_type="Button"
        )
                
        is_exist = ok_button.exists(timeout=10)
        print(f"[세션 이름:]필드 존재 여부: {is_exist}")
        
        print(f"[{TITLE}] 버튼 찾기 시작")
        ok_button.wait(wait_for="exists enabled visible ready", timeout=60)
        
        ok_button.click_input()
        
        print(f"[{TITLE}] 버튼 클릭 성공")

   
    except Exception as e:
        print(f"OK 버튼 클릭 실패: {e}")