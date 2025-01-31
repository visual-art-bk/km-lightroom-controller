# import time
# from pywinauto import WindowSpecification
# from .get_capture_settings_win import get_capture_settings_win

# def _check_win_sepc(win_spec: WindowSpecification):
#     return win_spec.exists(timeout=10)


# def input_username(
#     session_name, lightroom: WindowSpecification
# ):
#     print("성함+전화번호뒷자리 4자리 입력시작...")

#     try:
#         if lightroom.exists(timeout=10) == False:
            

#         # # 'Session Name:' 입력 필드 찾기
#         # session_name_edit = settings.child_window(
#         #     title="Session Name:",
#         #     auto_id="65535",
#         #     control_type="Edit",
#         # )

#         # settings.exists(timeout=10)
#         # # 입력 필드가 활성화될 때까지 대기
#         # session_name_edit.wait("ready", timeout=5)

#         # # 기존 값 지우기 (필요 시)
#         # session_name_edit.set_text("")  # 기존 값 제거
#         # session_name_edit.set_text(session_name)  # 새로운 값 입력

#     except Exception as e:
#         print(f"OK 버튼 클릭 실패: {e}")
