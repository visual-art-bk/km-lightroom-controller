import threading
import tkinter as tk
from tkinter import messagebox
import lightroom  # 기존의 Lightroom 연결 함수
from gui_utils.overlay.OverlayWindow import OverlayWindow

class LightroomApp:
    """Lightroom 실행 GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("Lightroom 실행기")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        # 사용자 입력 라벨
        self.label = tk.Label(root, text="사용자 이름을 입력하세요:")
        self.label.pack(pady=10)

        # 사용자 입력 필드
        self.entry = tk.Entry(root, width=25)
        self.entry.pack(pady=5)

        # 실행 버튼
        self.run_button = tk.Button(root, text="Lightroom 실행", command=self.run_lightroom)
        self.run_button.pack(pady=10)

    def run_lightroom(self):
        """ 사용자가 입력한 값을 `connect_lightroom()`에 전달하여 실행 """
        username = self.entry.get().strip()

        if not username:
            messagebox.showwarning("입력 오류", "사용자 이름을 입력하세요!")
            return

        print(f"[🚀] Lightroom을 {username} 사용자로 실행합니다...")

        # Lightroom 실행을 별도 스레드에서 실행 (UI가 멈추지 않도록 처리)
        threading.Thread(target=self.connect_lightroom, args=(username,), daemon=True).start()

    def connect_lightroom(self, username):
        """Lightroom 자동화 실행 (스레드 내부 실행)"""
        try:
            print(f"[⏳] Lightroom 자동화 시작: {username}")
            lightroom.init(username)  # Lightroom 자동화 시작
            messagebox.showinfo("완료", f"Lightroom 자동화 완료: {username}")
            print(f"[✅] Lightroom 자동화 완료: {username}")
        except Exception as e:
            messagebox.showerror("오류", f"Lightroom 실행 실패: {e}")
            print(f"[❌] Lightroom 자동화 실패: {e}")

if __name__ == "__main__":
    # Tkinter 메인 루프 생성
    root = tk.Tk()
    root.withdraw()  # 기본 Tk 창 숨기기

    # 오버레이 창 생성 (메인 스레드에서 실행)
    overlay = OverlayWindow.create_overlay(
        width=1400,
        height=200,
        bg_color="red",
        text="다른 설정은 절대!!! 건드리지 마세요!",
        text_color="yellow",
        font_size=40,
        animation_speed=20,
    )

    # Lightroom 실행기 GUI 띄우기
    app_window = tk.Toplevel()  # 새로운 Tk 창 생성
    app = LightroomApp(app_window)

    root.mainloop()  # Tkinter 메인 루프 실행
