import time
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
from .click_capture import click_capture
from .click_tet_capture_settings import click_tet_capture_settings
from .click_start_tet_capture import click_start_tet_capture
from .cilck_tet_settings_ok import cilck_tet_settings_ok
from .input_username import input_username

def connect_lightroom(username):
    app = Application(backend="uia").start(
        r"C:\Program Files\Adobe\Adobe Lightroom Classic\Lightroom.exe"
    )

    print(f"입력받은 사용자이름 {username}")

    # Lightroom 메인 창 연결
    lightroom = app.window(title_re=".*Lightroom Classic.*")
    lightroom.wait("ready", timeout=10000)  # 창이 준비될 때까지 대기

    click_capture(lightroom)

    click_start_tet_capture(lightroom)
  
    settings = click_tet_capture_settings(lightroom)

    input_username(session_name=username, settings=settings)
   
    cilck_tet_settings_ok(settings)


__all__ = ["connect_lightroom"]
