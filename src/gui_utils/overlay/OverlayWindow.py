import tkinter as tk


class OverlayWindow(tk.Toplevel):
    _instance = None  # 싱글턴 인스턴스 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OverlayWindow, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        master=None,
        width=500,
        height=250,
        bg_color="black",
        text="Hello, Overlay!",
        text_color="white",
        font_size=30,
        animation_speed=10,
    ):
        if hasattr(self, "_initialized") and self._initialized:
            return  # 이미 초기화된 경우 중복 실행 방지

        super().__init__(master)

        self._initialized = True
        self.title("오버레이 창")

        # 크기 및 속성 설정
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.animation_speed = animation_speed  # 애니메이션 속도 (낮을수록 빠름)

        # 창 속성 설정
        self.geometry(f"{width}x{height}+0+0")
        self.configure(bg=self.bg_color)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.6)  # 반투명도
        self.overrideredirect(True)  # 창의 타이틀 바 제거
        self.bind("<Escape>", lambda e: None)  # ESC 키 방지
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # 창을 완전히 업데이트한 후 정확한 위치로 이동
        self.update_idletasks()
        self.center_window()

        # 캔버스 생성 (텍스트 애니메이션용)
        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            bg=self.bg_color,
            highlightthickness=0,
        )
        self.canvas.pack()

        # 애니메이션 텍스트 추가 (왼쪽 바깥에서 시작)
        self.text_id = self.canvas.create_text(
            -self.width // 2,
            self.height // 2,
            text=self.text,
            font=("Arial", self.font_size, "bold"),
            fill=self.text_color,
            anchor="w",
        )

        # 애니메이션 시작
        self.animate_text()

    def center_window(self):
        """창을 화면 중앙에 배치하는 함수"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_coord = (screen_width - self.width) // 2
        y_coord = (screen_height - self.height) // 2

        self.geometry(f"{self.width}x{self.height}+{x_coord}+{y_coord}")

    def animate_text(self):
        """텍스트를 왼쪽에서 오른쪽으로 이동 후 다시 처음으로 재배치하는 애니메이션"""
        current_x, _ = self.canvas.coords(self.text_id)

        if current_x < self.width:
            self.canvas.move(self.text_id, 5, 0)  # 오른쪽으로 이동
        else:
            self.canvas.coords(
                self.text_id, -self.width // 2, self.height // 2
            )  # 왼쪽 처음으로 되돌리기

        self.after(self.animation_speed, self.animate_text)  # 일정 간격으로 반복 실행

    def on_close(self):
        """창 닫기 이벤트 핸들러"""
        self.destroy()
        OverlayWindow._instance = None  # 싱글턴 해제

    @classmethod
    def create_overlay(
        cls,
        width=500,
        height=250,
        bg_color="black",
        text="Hello, Overlay!",
        text_color="white",
        font_size=30,
        animation_speed=10,
    ):
        """싱글턴 방식으로 오버레이 창을 생성"""
        if cls._instance is None:
            cls._instance = OverlayWindow(
                width=width,
                height=height,
                bg_color=bg_color,
                text=text,
                text_color=text_color,
                font_size=font_size,
                animation_speed=animation_speed,
            )
        return cls._instance

    @classmethod
    def close_overlay(cls):
        """오버레이 창을 닫는 메서드"""
        if cls._instance:
            print("오버레이 창 닫기 시도")
            cls._instance.quit()
            cls._instance.destroy()
            cls._instance = None
            print("오버레이 창이 정상적으로 닫혔습니다.")
        else:
            print("오버레이 창이 이미 닫혀 있음.")
