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
from PySide6.QtCore import QThread, Signal, Qt
from StateManager import StateManager, AppState
import lightroom


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

        self.label = QLabel("사용자 이름을 입력하세요:")
        layout.addWidget(self.label)

        self.entry = QLineEdit()
        layout.addWidget(self.entry)

        self.run_button = QPushButton("Lightroom 실행")
        self.run_button.clicked.connect(self.run_lightroom)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_lightroom(self):
        """사용자가 입력한 값을 `LightroomThread`에 전달하여 실행"""
        username = self.entry.text().strip()

        if not username:
            QMessageBox.warning(self, "입력 오류", "사용자 이름을 입력하세요!")
            return

        # 🔄 전역 상태 업데이트 (RxPy 자동 반영)
        self.state_manager.update_state(username=username, lightroom_running=True)

        # Lightroom 실행을 백그라운드에서 실행
        self.thread = LightroomThread(username)
        self.thread.finished.connect(self.on_lightroom_finished)
        self.thread.start()

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
        print(f"[📢] 상태 변경 감지: {new_state}")

        if new_state.export_completed:
            QMessageBox.information(
                self,
                "내보내기 완료",
                f"파일이 내보내졌습니다: {new_state.export_filename}",
            )
            print(f"[✅] 최종 상태 → {new_state}")
