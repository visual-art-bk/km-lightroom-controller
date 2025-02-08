from pywinauto import WindowSpecification


def set_template(win_spects: WindowSpecification):
    template_combo = win_spects.child_window(title="템플릿:", control_type="ComboBox")
    template_combo.select("사용자 정의 이름 - 원본 파일 번호")



    edit_field = win_spects.child_window(
        title="사용자 정의 텍스트:", control_type="Edit"
    )
    edit_field.set_text("원본")
