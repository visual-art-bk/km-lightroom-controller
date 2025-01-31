from pywinauto import WindowSpecification

TITLE = "세션 이름:"


def input_session_id(win_specs: WindowSpecification, session_id="정의되지않음"):
    print(f"[{TITLE}] 필드 입력 시작")

    try:
        print(f"[{TITLE}] 필드 생성 시작")
        
        session_id_filed = win_specs.child_window(
            title=TITLE, auto_id="65535", control_type="Edit"
        )
        
        
        is_exist = session_id_filed.exists(timeout=10)
        print(f"[세션 이름:]필드 존재 여부: {is_exist}")
        
        
        print(f"[{TITLE}] 필드 찾기 시작")
        session_id_filed.wait(wait_for="exists enabled visible ready", timeout=60)

        # 기존 값 지우기
        session_id_filed.set_text("")
        
        # 새로운 값 입력
        session_id_filed.set_text(session_id)

        print(f"[{TITLE}] 필드 입력 성공")

    except Exception as e:
        print(f"[{TITLE}] 필드 입력 실패: {e}")