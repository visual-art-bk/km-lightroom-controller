import time

def click_start_tet_capture(lightroom):
    tether_window = lightroom.window(title_re=".*Start Tethered Capture.*")
    tether_window.wait("visible", timeout=1000)
    tether_window.click_input()