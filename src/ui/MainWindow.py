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
from StateManager import StateManager, AppState
import lightroom
from ui.overlay.OverlayWindow import OverlayWindow
from monitorings.LightroomMonitorThread import LightroomMonitorThread


class LightroomThread(QThread):
    """Lightroom 실행을 백그라운드에서 처리하는 스레드"""

    finished = Signal(str)

    def __init__(self, username: str):
        super().__init__()
        self.username = username

    def run(self):
        """Lightroom 실행 및 상태 관리"""
        try:
            print(f"[🚀] Lightroom 실행 시작: {self.username}")
            lightroom.init(self.username)  # Lightroom 자동화 실행

            export_filename = f"{self.username}_exported.jpg"
            self.finished.emit(export_filename)  # UI에 성공 이벤트 전달

        except Exception as e:
            self.finished.emit(f"ERROR: {str(e)}")  # 오류 이벤트 전달


class MainWindow(QMainWindow):
    """Lightroom 실행 GUI"""

    def __init__(self, x=None, y=0, width=300, height=200):
        super().__init__()

        self.setWindowTitle("Lightroom 실행기")

        # ✅ 항상 최상단에 고정
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # ✅ 현재 화면 크기 가져오기
        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()  # 화면 전체 너비

        # ✅ 사용자가 x를 설정하지 않으면 기본값으로 "우측 상단" 위치 지정
        if x is None:
            x = screen_width - width  # 우측 끝으로 정렬

        # ✅ 창의 초기 위치 및 크기 설정 (기본값: 화면 우측 상단)
        self.setGeometry(x, y, width, height)

        # ✅ 전역 상태 관리자
        self.state_manager = StateManager()
        self.state_manager.subscribe(self.on_state_change)  # 상태 변경 구독

        # ✅ UI 레이아웃 설정
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
        self.run_button.clicked.connect(self.run_lightroom)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.overlay = None
        self.lightroom_monitor = None

    def init_state(self):

        self.overlay = None
        # OverlayWindow._instance = None
        self.state_manager.update_state(
            phone_number="",
            username="",
            context="상태 초기화",
            lightroom_running=False,
            overlay_running=False,
        )

    def run_lightroom(self):
        self.init_state()

        """사용자가 입력한 값을 `LightroomThread`에 전달하여 실행"""
        username = self.username_entry.text().strip()
        phone_number = self.phone_number_entry.text().strip()

        if not username:
            QMessageBox.warning(self, "입력 오류", "사용자 이름을 입력하세요!")
            return

        if not phone_number:
            QMessageBox.warning(
                self, "입력 오류", "전화번호 뒷자리 4자리를 입력하세요!"
            )
            return

        # 🔄 전역 상태 업데이트 (RxPy 자동 반영)
        self.state_manager.update_state(
            phone_number=phone_number,
            username=username,
            context="사용자정보입력 상태",
        )

        # Lightroom 실행을 백그라운드에서 실행
        self.thread = LightroomThread(username)
        self.thread.finished.connect(self.on_lightroom_finished)
        self.thread.start()

        # 🔄 전역 상태 업데이트 (RxPy 자동 반영)
        self.state_manager.update_state(
            context="라이트룸실행 상태",
            lightroom_running=True,
        )

        time.sleep(1.5)

        # self.create_overlay()

        self.state_manager.update_state(
            context="오버레이실행 상태",
            overlay_running=True,
        )

        # ✅ Lightroom 실행 감지 스레드 시작
        self.lightroom_monitor = LightroomMonitorThread()
        self.lightroom_monitor.lightroom_closed.connect(self.close_main_window)
        self.lightroom_monitor.start()

    def create_overlay(self):
        """✅ `overlay_running=True`이면 OverlayWindow 생성"""
        if self.overlay is None:
            self.overlay = OverlayWindow.create_overlay(
                width=1200,
                height=550,
                bg_color="#FFFFFF",
                opacity=0.3,
                text="⚠ 경고: 설정을 변경하지 마세요!",
                text_color="black",
                font_size=48,
                animation_speed=25,
                y_offset=50,
                blur_radius=50,
            )
            self.overlay.show()
        else:
            print("해당없음")

    def close_main_window(self):
        """✅ Lightroom이 종료되면 MainWindow도 종료"""
        print("✅ MainWindow 종료 실행!")
        self.close()

    def on_lightroom_finished(self, result: str):
        """Lightroom 실행 완료 후 UI 업데이트"""
        if result.startswith("ERROR"):
            QMessageBox.critical(self, "오류", f"Lightroom 실행 실패: {result[6:]}")
            self.state_manager.update_state(
                lightroom_running=False
            )  # 오류 시 상태 변경
        else:
            QMessageBox.information(self, "완료", f"Lightroom 자동화 완료: {result}")
            self.state_manager.update_state(
                export_filename=result, export_completed=True, lightroom_running=False
            )

    def on_state_change(self, new_state: AppState):
        """전역 상태 변경 감지 및 UI 반영"""
        print(f"---> [📢] 상태 변경 감지: {new_state.context}")
        print(f"사용자이름: {new_state.username}")
        print(f"전화번호: {new_state.phone_number}")
        print(f"라이트룸 실행여부: {'실행' if new_state.lightroom_running else '중지'}")
        print(f"오버레이이 실행여부: {'실행' if new_state.overlay_running else '중지'}")
        print(f"                                                      ")

        if (
            new_state.overlay_running == False
            and OverlayWindow._instance
            # and new_state.lightroom_running == True
        ):

            print(f"✅ 오버레이 창 닫기 실행!")

            QMetaObject.invokeMethod(
                OverlayWindow._instance, "close", Qt.QueuedConnection
            )

            OverlayWindow._instance = None  # ✅ 싱글턴 객체 초기화

            self.state_manager.update_state(
                context="오버레이 종료 상태",
                lightroom_running=True,
                overlay_running=False,
            )
