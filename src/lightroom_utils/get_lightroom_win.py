from pywinauto import Application, WindowSpecification


def get_lightroom_win(app: Application) -> WindowSpecification:
    lightroom = app.window(title_re=".*Lightroom Classic.*")
    lightroom.wait("exists enabled visible ready", timeout=60)  # 창이 준비될 때까지 대기
    print('라이트룸 창 준비완료')
    return lightroom
