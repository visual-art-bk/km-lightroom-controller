import time
import threading
from pynput import mouse
import ctypes
import sys

class MouseLocker:
    def __init__(self):
        """ 마우스 클릭 및 이동을 차단하는 리스너 """
        self.listener = mouse.Listener(on_move=self.block_move, on_click=self.block_click)
        self.locked = False  # 마우스 잠금 여부
        self.listener_thread = threading.Thread(target=self.start_listener, daemon=True)

    def block_click(self, x, y, button, pressed):
        """ 마우스 클릭 차단 """
        if self.locked:
            print(f"[🔒] 마우스 클릭 차단됨: {button} at ({x}, {y})")
            return False  # 클릭 차단
        return True

    def block_move(self, x, y):
        """ 마우스 이동 차단 """
        if self.locked:
            print(f"[🔒] 마우스 이동 차단됨 at ({x}, {y})")
            return False  # 이동 차단
        return True

    def start_listener(self):
        """ 리스너를 별도 스레드에서 실행 (stop 호출 전까지 종료되지 않도록) """
        print("[🔒] 마우스 리스너 실행됨 (백그라운드)")
        self.listener.start()  # 이걸 실행하면 join()이 필요 없음 (자동 유지됨)

    def start(self):
        """ 마우스 이벤트 리스너 시작 (백그라운드 스레드 실행) """
        self.listener_thread.start()
        time.sleep(1)  # 리스너가 제대로 실행될 시간을 확보

    def lock_mouse(self):
        """ 마우스 잠금 활성화 """
        self.locked = True
        print("[🔒] 마우스 입력 차단됨")

    def unlock_mouse(self):
        """ 마우스 잠금 해제 """
        self.locked = False
        print("[🔓] 마우스 입력 허용됨")

    def stop(self):
        """ 리스너 종료 """
        self.listener.stop()
        print("[❌] 마우스 리스너 종료됨")

def is_admin():
    """ 현재 실행 중인 프로세스가 관리자 권한인지 확인 """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """ 관리자 권한이 없으면 자동으로 관리자 권한으로 실행 """
    if not is_admin():
        print("[⚠️] 관리자 권한이 필요합니다. 다시 실행합니다...")

        # 현재 Python 실행 파일을 관리자 권한으로 다시 실행
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )

        sys.exit(0)  # 현재 실행 중인 프로세스를 종료하고 재실행
