from pywinauto import WindowSpecification
from pywinauto.keyboard import send_keys
from pywinauto import WindowSpecification


def open_export_window(lightroom: WindowSpecification):
    """✅ Lightroom에서 'Ctrl + Shift + E' 단축키를 사용하여 '내보내기(E)...' 창 열기"""
    export_window = lightroom.child_window(
        title_re=r"\d+개의 파일 내보내기", control_type="Window"
    )
    if export_window.exists():
        print("✅ '내보내기' 창 감지 완료!")
        return export_window
    else:
        print("내보내기 창 없음")
