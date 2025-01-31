import tkinter as tk

WIDTH = 1000
HEIGHT = 500
X_COORD = 100
Y_COORD = 100


class OverlayWindow(tk.Toplevel):
    _instance = None  # 싱글턴 인스턴스 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OverlayWindow, cls).__new__(cls)
        return cls._instance

    def __init__(self, master=None):
        if hasattr(self, "_initialized") and self._initialized:
            return  # 이미 초기화된 경우 중복 실행 방지

        super().__init__(master)

        self._initialized = True
        self.title("오버레이 창")
        self.geometry(f"{WIDTH}x{HEIGHT}+{X_COORD}+{Y_COORD}")  # 크기 및 위치 설정
        self.configure(bg="black")  # 배경색 설정

        # 항상 위에 유지, 반투명 설정
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.6)  # 반투명도 (0: 완전 투명, 1: 불투명)

        # 전체 화면 클릭 방지
        self.overrideredirect(True)  # 창의 타이틀 바 제거

        # ESC 키를 눌러도 창이 닫히지 않도록 방지
        self.bind("<Escape>", lambda e: None)

        # 윈도우 닫기 이벤트 핸들러 설정
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """창 닫기 이벤트 핸들러"""
        self.destroy()
        OverlayWindow._instance = None  # 싱글턴 해제

    @classmethod
    def create_overlay(cls):
        """싱글턴 방식으로 오버레이 창을 생성"""
        if cls._instance is None:
            cls._instance = OverlayWindow()
        return cls._instance

    @classmethod
    def close_overlay(cls, delay=0.5):
        """오버레이 창을 닫는 메서드"""
        if cls._instance:
            print("오버레이 창 닫기 시도")
            cls._instance.quit()  # mainloop 종료
            cls._instance.destroy()  # 창 제거
            cls._instance = None  # 싱글턴 해제
            print("오버레이 창이 정상적으로 닫혔습니다.")
        else:
            print("오버레이 창이 이미 닫혀 있음.")
