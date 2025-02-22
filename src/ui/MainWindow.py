from constants import (
    MAIN_WINDOW_BG_COLOR,
    SIGNAL_NO_DETECTED_CAMERA,
    SIGNAL_NO_SEARCHED_CAMERA,
    SIGNAL_LIGHTROOM_LAUHCNER_START_FAILED,
    SIGNAL_LIGHTROOM_AUTOMATION_CONNECT_FAILED,
    SIGNAL_LIGHTROOM_AUTOMATION_FOCUS_FAILED,
    SIGNAL_LIGHTROOM_AUTOMATION_CONTROL_FAILED
)
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QApplication,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from state_manager import StateManager, AppState
from lightroom import LightroomAutomationThread, LightroomLaunchThread
from ui.overlay.OverlayWindow import OverlayWindow
from helpers.log_exception_to_file import log_exception_to_file
from ui.msg_box import create_error_msg
from ui.inputs.input_main_field import input_main_field
from ui.buttons.btn_run_main import btn_run_main
from ui.msg_box.show_guide import show_guide


class MainWindow(QMainWindow):
    """Lightroom 실행 GUI"""

    def __init__(self, x=None, y=0, width=300, height=200):
        super().__init__()

        self.init_state_manager()

        self.setWindowTitle("다비 촬영 매니저")

        self.setWindowIcon(QIcon("assets/다비스튜디오_logo11_black_ico.ico"))

        self.setObjectName("MainWindow")
        self.setStyleSheet(
            f"""
            #MainWindow {{
                background-color: {MAIN_WINDOW_BG_COLOR};
            }}
            """
        )

        self.init_window_position(height=height, width=width)

        self.init_window_layout()

        self.overlay_window = None
        self.thread_lightroom_automation = None

    def init_input_main_fields(self, layout):
        self.input_username = input_main_field(
            layout=layout,
            label="예약자 성함",
            placeholder="“여기에 입력하세요.”",
        )
        self.input_phone = input_main_field(
            layout=layout,
            label="전화번호 뒷자리 4자리",
            placeholder="“여기에 입력하세요.”",
        )

    def init_window_layout(self):
        layout = QVBoxLayout()

        self.init_input_main_fields(layout=layout)

        self.run_button = btn_run_main()
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
        # 현재 화면의 해상도 가져오기
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

    def get_user_infos(self):
        return {
            "username": self.username_entry.text().strip(),
            "phone_number": self.phone_number_entry.text().strip(),
        }

    def on_lightroom_launcher_start(self):
        if (
            self.thread_lightroom_launcher.lightroom_started
            == SIGNAL_LIGHTROOM_LAUHCNER_START_FAILED
        ):
            print("Main-라이트룸 실행 실패!")
            self.show_guide_msg(msg_code=SIGNAL_LIGHTROOM_LAUHCNER_START_FAILED)
            self.cleanup_resources()
            return

        print("Main-라이트룸 실행 성공")
        self.thread_lightroom_automation.start()

    def init_threads(self):
        self.thread_lightroom_launcher = LightroomLaunchThread()
        self.thread_lightroom_automation = LightroomAutomationThread()

        self.thread_lightroom_launcher.lightroom_started.connect(
            self.on_lightroom_launcher_start
        )

        self.thread_lightroom_automation.finished.connect(
            self.on_lightroom_automation_finished
        )

        self.thread_lightroom_automation.failed.connect(
            self.on_lightroom_automation_failed
        )

        self.thread_lightroom_launcher.start()

    def run_main_window(self):
        try:
            username = self.input_username.text().strip()
            phone_number = self.input_phone.text().strip()

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
        except Exception as e:
            log_exception_to_file(
                exception_obj=e,
                message="메인 윈도우에서 run_main_window 실행 중 에러발생생",
            )

    def create_overlay(self):
        """독립적인 오버레이 창을 생성하고 부모 윈도우와 시그널 연결"""
        if self.overlay_window is not None:
            print("이미 오버레이가 생성 중입니다.")
            return

        self.overlay_window = OverlayWindow()  #  독립적인 오버레이 생성
        self.overlay_window.show()

    def on_lightroom_automation_failed(self, failed):
        self.show_guide_msg(msg_code=failed)
        self.cleanup_resources()

    def on_lightroom_automation_finished(self, is_finished):
        self.raise_()  # ✅ 메인 윈도우를 최상위로 올림
        self.activateWindow()  # ✅ 메인 윈도우에 포커스 활성화

        if is_finished:
            show_guide(self, file_path="메시지/안내메세지.txt")
        else:
            self.show_guide_msg(
                msg="⚠️ 연결된 카메라가 없어요. 다비 고객센터에 연락주세요. ⚠️"
            )

        self.cleanup_resources()

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

    def show_guide_msg(self, msg_code=""):
        self.raise_()  # ✅ 메인 윈도우를 최상위로 올림
        self.activateWindow()  # ✅ 메인 윈도우에 포커스 활성화

        if msg_code == SIGNAL_NO_DETECTED_CAMERA:
            show_guide(parent=self, file_path="메시지/카메라감지실패메시지.txt")
        elif msg_code == SIGNAL_NO_SEARCHED_CAMERA:
            show_guide(parent=self, file_path="메시지/카메라감지실패메시지.txt")
        elif msg_code == SIGNAL_LIGHTROOM_AUTOMATION_CONNECT_FAILED:
            show_guide(
                parent=self,
                file_path="",
                defalut_message="⚠️⚠️⚠️ 라이트룸을 다시 실행해주세요.",
            )
        elif msg_code == SIGNAL_LIGHTROOM_AUTOMATION_FOCUS_FAILED:
            show_guide(
                parent=self,
                file_path="",
                defalut_message="⚠️⚠️⚠️ 라이트룸의 모든 창을 닫고 프로그램을 다시 실행해주세요.",
            )

        else:
            error_msg_box = create_error_msg(
                parent=self,
                content="⚠️ 촬영 셋팅 중 오류 발생! 프로그램을 재실행해주세요.",
            )
            error_msg_box.exec()

    def closeEvent(self, event):
        """메인 윈도우가 닫힐 때 모든 리소스 정리"""
        print(" 프로그램 종료: 모든 리소스 정리 중...")

        self.cleanup_resources()

        print(" 모든 리소스 정리 완료. 프로그램 종료.")
        event.accept()  #  정상적으로 창을 닫음

    def cleanup_resources(self):
        """💡 프로그램 종료 전 모든 리소스를 완전히 정리하는 함수"""
        print("🔄 모든 리소스 정리 중...")

        # ✅ 1. Lightroom 실행 스레드 정리
        if self.thread_lightroom_launcher:
            if self.thread_lightroom_launcher.isRunning():
                print("⚠️ Lightroom 실행 스레드 강제 종료")
                self.thread_lightroom_launcher.terminate()
                self.thread_lightroom_launcher.wait()  # ✅ 강제 종료 후 대기
            self.thread_lightroom_launcher = None

        # ✅ 2. Lightroom 자동화 스레드 정리
        if self.thread_lightroom_automation:
            if self.thread_lightroom_automation.isRunning():
                print("⚠️ Lightroom 자동화 스레드 강제 종료")
                self.thread_lightroom_automation.terminate()
                self.thread_lightroom_automation.wait(
                    2000
                )  # ✅ 강제 종료 후 최대 2초 대기
            self.thread_lightroom_automation = None

        # ✅ 3. 오버레이 창 닫기
        if self.overlay_window:
            print("⚠️ 오버레이 스레드 강제 종료")
            self.overlay_window.close()
            self.overlay_window.deleteLater()
            self.overlay_window = None

        # ✅ 4. 상태 관리자 해제
        self.state_manager = None

        # ✅ 5. UI 종료
        self.deleteLater()  # ✅ UI 객체 제거 예약 (먼저 호출)
        self.close()  # ✅ UI 창 닫기

        print("✅ 모든 리소스 정리 완료. 프로그램 종료.")
