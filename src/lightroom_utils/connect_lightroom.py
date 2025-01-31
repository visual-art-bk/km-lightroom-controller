
def connect_lightroom(username):
    app = Application(backend="uia").start(
        r"C:\Program Files\Adobe\Adobe Lightroom Classic\Lightroom.exe"
    )

    print(f"입력받은 사용자이름 {username}")

    # Lightroom 메인 창 연결
    lightroom = app.window(title_re=".*Lightroom Classic.*")
    lightroom.wait("ready", timeout=30)  # 창이 준비될 때까지 대기
    return lightroom, app

