import tkinter as tk
from tkinter import messagebox
import lightroom   # 기존의 Lightroom 연결 함수

# Tkinter 창 생성
# class LightroomApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Lightroom 실행기")  # 창 제목
#         self.root.geometry("300x200")  # 창 크기
#         self.root.resizable(False, False)  # 창 크기 고정

#         # 라벨
#         self.label = tk.Label(root, text="사용자 이름을 입력하세요:")
#         self.label.pack(pady=10)

#         # 입력 필드
#         self.entry = tk.Entry(root, width=25)
#         self.entry.pack(pady=5)

#         # 실행 버튼
#         self.run_button = tk.Button(root, text="Lightroom 실행", command=self.run_lightroom)
#         self.run_button.pack(pady=10)

#     def run_lightroom(self):
#         """ 사용자가 입력한 값을 `connect_lightroom()`에 전달하여 실행 """
#         username = self.entry.get()
#         if not username.strip():
#             messagebox.showwarning("입력 오류", "사용자 이름을 입력하세요!")
#             return

#         print(f"[🚀] Lightroom을 {username} 사용자로 실행합니다...")
#         connect_lightroom(username)  # 입력값을 connect_lightroom()에 전달
#         messagebox.showinfo("완료", f"Lightroom 실행 완료: {username}")

if __name__ == "__main__":
    lightroom.init('test123')
    # root = tk.Tk()
    # app = LightroomApp(root)
    # root.mainloop()
