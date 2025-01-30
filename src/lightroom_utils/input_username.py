import time

def input_username(settings, session_name):
    try:
        if settings == None:
            print('셋팅 값이 올바르지 않습니다.')
            return 
        
        print('이름 입력중...')
      
        # 'Session Name:' 입력 필드 찾기
        session_name_edit = settings.child_window(title="Session Name:", auto_id="65535", control_type="Edit")

        # 입력 필드가 활성화될 때까지 대기
        session_name_edit.wait("ready", timeout=5)

        # 기존 값 지우기 (필요 시)
        session_name_edit.set_text("")  # 기존 값 제거
        session_name_edit.set_text(session_name)  # 새로운 값 입력
   
    except Exception as e:
        print(f"OK 버튼 클릭 실패: {e}")