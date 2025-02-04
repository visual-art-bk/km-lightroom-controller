import time
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QApplication,
)
from PySide6.QtCore import QThread, Signal, Qt, QMetaObject
from state_manager import StateManager, AppState
from lightroom import LightroomAutomationThread, LightroomLaunchThread
from ui.overlay.OverlayWindow import OverlayWindow
from monitorings.LightroomMonitorThread import LightroomMonitorThread


class MainWindow(QMainWindow):
    """Lightroom 실행 GUI"""

    def __init__(self, x=None, y=0, width=300, height=200):
        super().__init__()

        self.init_state_manager()

        self.setWindowTitle("라이트룸 촬영 매니저")

        self.init_window_position(
            height=height, x=x, screen_width=self.get_screen_width(), width=width, y=y
        )

        self.init_window_layout()

        self.overlay_window = None
        self.lightroom_monitor = None
        self.thread_lightroom_automation = None

    def init_window_layout(self):
        layout = QVBoxLayout()

        self.label_username = QLabel("예약자 이름")
        layout.addWidget(self.label_username)

        self.username_entry = QLineEdit()
        layout.addWidget(self.username_entry)

        self.label_phone_number = QLabel("전화번호 뒷자리 4자리")
        layout.addWidget(self.label_phone_number)

        self.phone_number_entry = QLineEdit()
        layout.addWidget(self.phone_number_entry)

        self.run_button = QPushButton("Lightroom 실행")
        self.run_button.clicked.connect(self.run_main_window)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_state_manager(self):
        self.state_manager = StateManager()
        self.state_manager.subscribe(self.ON_STATE_CHANGE)  # 상태 변경 구독

    def init_window_position(self, x, y, width, height, screen_width):
        # 항상 최상단에 고정
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # ✅ 사용자가 x를 설정하지 않으면 기본값으로 "우측 상단" 위치 지정
        if x is None:
            x = screen_width - width  # 우측 끝으로 정렬

        # ✅ 창의 초기 위치 및 크기 설정 (기본값: 화면 우측 상단)
        self.setGeometry(x, y, width, height)

    def get_screen_width(self):
        # 현재 화면 크기 가져오기
        screen = QApplication.primaryScreen().availableGeometry()
        return screen.width()  # 화면 전체 너비

    def delete_overlay(self):
        self.overlay_window = None
        OverlayWindow._instance = None

    def get_user_infos(self):
        return {
            "username": self.username_entry.text().strip(),
            "phone_number": self.phone_number_entry.text().strip(),
        }

    def init_threads(self):
        self.thread_lightroom_launcher = LightroomLaunchThread()
        self.thread_lightroom_automation = LightroomAutomationThread()
        self.thread_lightroom_mornitor = LightroomMonitorThread()

        self.thread_lightroom_automation.finished.connect(
            self.on_lightroom_automation_finished
        )
        self.thread_lightroom_automation.adobe_note_closed.connect(
            self.on_lightroom_launcher_started
        )
        self.thread_lightroom_mornitor.lightroom_closed_mornitoring.connect(
            self.on_lightroom_closed_mornitoring
        )

        self.thread_lightroom_launcher.start()
        self.thread_lightroom_automation.start()

    def run_main_window(self):
        userer_infos = self.get_user_infos()
        username = userer_infos["username"]
        phone_number = userer_infos["phone_number"]

        if username == "":
            QMessageBox.warning(self, "입력 오류", "사용자 이름을 입력하세요!")
            return

        if phone_number == "":
            QMessageBox.warning(
                self, "입력 오류", "전화번호 뒷자리 4자리를 입력하세요!"
            )
            return

        self.state_manager.update_state(
            phone_number=phone_number,
            username=username,
            context="사용자정보 올바르게 입력함",
        )

        self.init_threads()

    def create_overlay(self, text="마우스 및 키보드를 절대 건들지 마세요 :)"):
        """✅ `overlay_running=True`이면 OverlayWindow 생성"""
        if self.overlay_window is None:
            self.overlay_window = OverlayWindow.create_overlay(
                width=1200,
                height=550,
                bg_color="#FFFFFF",
                opacity=0.3,
                text=text,
                text_color="black",
                font_size=48,
                animation_speed=25,
                y_offset=50,
                blur_radius=50,
            )
            self.overlay_window.show()
        else:
            print("해당없음")

    def on_lightroom_closed_mornitoring(self):
        pass

    def on_lightroom_automation_finished(self):
        # ✅ 기존 오버레이 삭제
        if self.overlay_window is not None:
            self.delete_overlay()

        self.state_manager.update_state(
            context="자동화 끝! 오버레이 종료",
            overlay_running=False,
        )

        self.hide()

    def on_lightroom_closed_mornitoring(self):
        print("✅ Lightroom 종료 감지 → 프로그램 종료")

        self.state_manager.update_state(
            context="Lightroom 종료 → 프로그램 종료",
            lightroom_running=False,
        )

        QApplication.quit()  # ✅ `QApplication` 종료 (완전히 종료)

    def on_lightroom_launcher_started(self, success):
        """✅ Lightroom 실행 완료 후 오버레이 실행"""
        if success:
            self.state_manager.update_state(
                context="Lightroom 실행 완료",
                lightroom_running=True,
            )

            time.sleep(2)

            self.create_overlay()

            self.state_manager.update_state(
                context="오버레이 실행 완료",
                overlay_running=True,
            )

            # ✅ Lightroom이 실행되면 종료 감지 스레드 시작
            self.thread_lightroom_mornitor.start()

        else:
            print("❌ Lightroom 실행 실패! 오버레이 실행 안 함")

    def ON_STATE_CHANGE(self, new_state: AppState):
        """전역 상태 변경 감지 및 UI 반영"""
        print(
            f"----------------- [📢] 상태 변경 감지: {new_state.context} -----------------"
        )
        print(f"사용자이름: {new_state.username}")
        print(f"전화번호: {new_state.phone_number}")
        print(f"라이트룸 실행여부: {'실행' if new_state.lightroom_running else '중지'}")
        print(f"오버레이 실행여부: {'실행' if new_state.overlay_running else '중지'}")
        print(f"                                                      ")
