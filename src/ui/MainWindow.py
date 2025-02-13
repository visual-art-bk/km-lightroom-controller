import os
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


class MainWindow(QMainWindow):
    """Lightroom 실행 GUI"""

    def __init__(self, x=None, y=0, width=300, height=200):
        super().__init__()

        self.init_state_manager()

        self.setWindowTitle("다비 촬영 매니저")

        self.init_window_position(
            height=height, width=width
        )

        self.init_window_layout()

        self.overlay_window = None
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

        self.run_button = QPushButton("📸 촬영 시작하기")
        self.run_button.clicked.connect(self.run_main_window)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_state_manager(self):
        self.state_manager = StateManager()
        self.state_manager.subscribe(self.ON_STATE_CHANGE)  # 상태 변경 구독

    def init_window_position(self, width, height):
        # 항상 최상단에 고정
        # ✅ 현재 화면의 해상도 가져오기
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # ✅ 창을 화면 정중앙에 배치 (좌우 & 상하)
        x = (screen_width - width) // 2  # 좌우 정가운데
        y = (screen_height - height) // 2  # 상하 정가운데


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

        self.thread_lightroom_automation.finished.connect(
            self.on_lightroom_automation_finished
        )
        self.thread_lightroom_automation.adobe_note_closed.connect(
            self.on_lightroom_launcher_started
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

        self.setWindowState(Qt.WindowMinimized)

        self.create_overlay()

    def create_overlay(self):
        """독립적인 오버레이 창을 생성하고 부모 윈도우와 시그널 연결"""
        if self.overlay_window is not None:
            print("이미 오버레이가 생성 중입니다.")
            return

        self.overlay_window = OverlayWindow()  #  독립적인 오버레이 생성
        self.overlay_window.show()


    def cleanup_and_exit(self):
        """💡 프로그램 종료 전 모든 리소스를 완전히 정리하는 함수"""
        print("🔄 모든 리소스 정리 중...")

        if self.thread_lightroom_launcher:
            if self.thread_lightroom_launcher.isRunning():
                self.thread_lightroom_launcher.terminate()
                print("⚠️ Lightroom 실행 스레드 강제 종료")
            self.thread_lightroom_launcher.quit()
            self.thread_lightroom_launcher.wait()
            self.thread_lightroom_launcher = None

        if self.thread_lightroom_automation:
            if self.thread_lightroom_automation.isRunning():
                self.thread_lightroom_automation.terminate()
                print("⚠️ Lightroom 자동화 스레드 강제 종료")

            self.thread_lightroom_automation.quit()
            self.thread_lightroom_automation.wait()
            self.thread_lightroom_automation = None

        if self.overlay_window:
            self.overlay_window.close()
            self.overlay_window.deleteLater()
            self.overlay_window = None
            print("⚠️ 오버레이이 스레드 강제 종료")

        # ✅ 3. 상태 관리자 해제
        self.state_manager = None

        # ✅ 4. UI 창 닫기
        self.close()
        self.deleteLater()  # UI 객체를 명시적으로 제거

        # ✅ 5. QApplication 완전 종료
        QApplication.quit()

        # ✅ 6. **운영체제 프로세스 강제 종료 (최후의 수단)**
        print("🚀 모든 리소스 해제 완료 → 시스템 프로세스 강제 종료")
        os._exit(0)  # 💀 시스템 차원에서 프로세스 완전 제거

    def on_lightroom_automation_finished(self):
        # ✅ 기존 오버레이 삭제
        if self.overlay_window is not None:
            self.delete_overlay()

        self.state_manager.update_state(
            context="자동화 끝! 오버레이 종료",
            overlay_running=False,
        )

        self.cleanup_and_exit()

    def on_lightroom_launcher_started(self, success):
        if success:
            self.state_manager.update_state(
                context="Lightroom 실행 완료",
                lightroom_running=True,
            )

   

            self.state_manager.update_state(
                context="오버레이 실행 완료",
                overlay_running=True,
            )

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
