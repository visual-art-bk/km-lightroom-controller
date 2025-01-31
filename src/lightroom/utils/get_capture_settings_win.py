def get_capture_settings_win(lightroom):
    dialog_window = lightroom.window(title_re=".*Tethered Capture Settings.*")

    dialog_window.wait("visible", timeout=5)  # 다이얼로그 창이 뜰 때까지 대기

    return dialog_window
