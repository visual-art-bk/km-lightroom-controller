from pywinauto import WindowSpecification


def check_camera(
    lightroom: WindowSpecification,
):
    checking_connected_camera = lightroom.child_window(
        title="카메라를 감지하는 중...", control_type="Text", found_index=0
    )

    return not checking_connected_camera.exists()
