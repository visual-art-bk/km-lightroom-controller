from pynput import keyboard

class TaskManagerDetector:
    def __init__(self, stop_callback):
        """✅ Ctrl + Alt + Delete 감지를 위한 클래스"""
        self.stop_callback = stop_callback
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.running = True  # ✅ 실행 여부 플래그

        # ✅ 키 상태 추적
        self.ctrl_pressed = False
        self.alt_pressed = False
        self.delete_pressed = False

    def on_press(self, key):
        """✅ 키가 눌렸을 때 실행"""
        try:
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.ctrl_pressed = True
            if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.alt_pressed = True
            if key == keyboard.Key.delete:
                self.delete_pressed = True
            
            # ✅ Ctrl + Alt + Delete 감지 시 콜백 실행
            if self.ctrl_pressed and self.alt_pressed and self.delete_pressed:
                print("⚠️ Ctrl + Alt + Delete 감지됨! 자동화 중지")
                self.stop_callback()
        except AttributeError:
            pass

    def on_release(self, key):
        """✅ 키가 떼어졌을 때 실행"""
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            self.ctrl_pressed = False
        if key in [keyboard.Key.alt_l, keyboard.Key.alt_r]:
            self.alt_pressed = False
        if key == keyboard.Key.delete:
            self.delete_pressed = False

    def start(self):
        """✅ 키 리스너 시작"""
        self.listener.start()

    def stop(self):
        """✅ 키 리스너 중지"""
        print("🛑 Ctrl + Alt + Delete 감지 스레드 종료")
        self.running = False
        self.listener.stop()
