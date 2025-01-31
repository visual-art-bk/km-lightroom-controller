import time
from .utils.LightroomApp import LightroomApp
from .utils.get_lightroom_win import get_lightroom_win
from .tet_capture.selects.select_file_menu import select_file_menu
from .tet_capture.selects.select_tet_capture import select_tet_capture
from .tet_capture.selects.select_start_tet_capture import select_start_tet_capture
from .tet_capture.finds.find_tet_capture_settings import find_tet_capture_settings
from .tet_capture.inputs.input_username import input_session_id
from .tet_capture.clicks.cilck_tet_capture_settings_ok import (
    cilck_tet_capture_settings_ok,
)


def run_tet_capture(username, app):
    lightroom = get_lightroom_win(app)

    select_file_menu(app)
    select_tet_capture(app)
    select_start_tet_capture(app)

    tet_capture_settings = find_tet_capture_settings(lightroom)
    input_session_id(win_specs=tet_capture_settings, session_id=username)
    cilck_tet_capture_settings_ok(win_specs=tet_capture_settings)


def init(username="정의되지않음"):
    lightroomApp = LightroomApp()
    lightroomApp.start()

    app = lightroomApp.get_app()
    run_tet_capture(username, app)

    time.sleep(30)


__all__ = ["init"]
