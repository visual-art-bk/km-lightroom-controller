from pywinauto import WindowSpecification

def find_tet_capture_settings(lightroom: WindowSpecification):
    try:
        tet_caputre_settings = lightroom.child_window(
            title="연결전송된 촬영 설정", control_type="Window"
        )

        is_exist = tet_caputre_settings.exists(timeout=10)
        
        if is_exist == False:
            print('! 연결전송된 촬영 설정 존재하지 않습니다.')
            
        return tet_caputre_settings
    except Exception as e:
        print(e)