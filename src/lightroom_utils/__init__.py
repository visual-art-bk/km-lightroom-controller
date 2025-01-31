import time
from .selects.select_file_menu import select_file_menu
from .selects.select_tet_capture import select_tet_capture

# from .cilck_tet_settings_ok import cilck_tet_settings_ok
# from .input_username import input_username
from .LightroomApp import LightroomApp


def connect_lightroom(username):
    lightroomApp = LightroomApp()

    lightroomApp.start()

    app = lightroomApp.get_app()

    select_file_menu(app)

  

    select_tet_capture(app)

    time.sleep(30)

    # select_start_tet_capture(lightroom)

    # input_username(session_name=username, lightroom=lightroom)

    # cilck_tet_settings_ok(settings)


__all__ = ["connect_lightroom"]
