import time

CAPTURE_FLOW = "File->Tethered Capture"
IMPORT_FLOW = "File->Auto Import"
EXP_PRESET_FLOW = "File->Export With Preset"




def click_capture(lightroom):
    try:
        lightroom.menu_select(CAPTURE_FLOW)

        time.sleep(3)

        print("File 메뉴를 성공적으로 클릭했습니다.")
    except Exception as e:
        print(f"File 메뉴 클릭 실패: {e}")
