import datetime
from typedefs.signal_types import TypeAutomationSignal, TypeSignalStatus
from constants.status_code import (
    CAMERA_NOT_DETECTED,
    CAMERA_NOT_SEARCHED,
    AUTOMATION_LIGHTROOM_FOCUS_FAILED_WITH_NOTE,
    AUTOMATION_APPLICATOIN_INIT_FAILED
)
from constants import (
    MAIN_WINDOW_BG_COLOR,
    SIGNAL_NO_DETECTED_CAMERA,
    SIGNAL_NO_SEARCHED_CAMERA,
    SIGNAL_LIGHTROOM_LAUHCNER_START_FAILED,
    SIGNAL_LIGHTROOM_AUTOMATION_CONNECT_FAILED,
    SIGNAL_LIGHTROOM_AUTOMATION_FOCUS_FAILED,
)
from constants.style_constants import (
    MAIN_WINDOW_HEIGHT,
    MAIN_WINDOW_WIDTH,
    RUN_BTN_PLAY_ICON_PATH,
    RUN_BTN_STOP_ICON_PATH,
    TOP_APP_BAR_CLOSE_ICON_PATH,
    TOP_APP_BAR_MINIMIZE_ICON_PATH,
    TOP_APP_BAR_MAIN_ICON_PATH,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QApplication,
    QHBoxLayout,
    QSizePolicy,
    QPushButton,
)

from PySide6.QtGui import QIcon, QCursor
from PySide6.QtCore import Qt, QSize, QTimer
from typedefs.main_window_types import SizeDict
from state_manager import StateManager, AppState
from lightroom import LightroomAutomationThread, LightroomLaunchThread
from helpers.log_exception_to_file import log_exception_to_file

from ui.overlay.OverlayWindow import OverlayWindow
from ui.msg_box import create_error_msg
from ui.display.main_display_widget import create_main_display_widget
from ui.inputs.input_main_field import input_main_field
from ui.inputs.input_container import input_container
from ui.buttons.create_btn_with_icon import create_btn_with_icon
from ui.buttons.btn_run_main import btn_run_main
from ui.msg_box.show_guide import show_guide
from ui.surfaces import create_shadow_widget, create_central_widget
from ui.effects import create_shadow_effect


class MainWindow(QMainWindow):
    def __init__(self, x=None, y=0, width=MAIN_WINDOW_WIDTH, height=MAIN_WINDOW_HEIGHT):
        super().__init__()
        self.init_state_manager()

        # ✅ 윈도우 타이틀 (선택 사항)
        self.setWindowTitle("다비 촬영 매니저")
        self.setWindowIcon(QIcon("assets/다비스튜디오_logo11_black_ico.ico"))
        main_window_obj_name = "MainWindow"
        self.setObjectName(main_window_obj_name)
        self.setStyleSheet(
            f"""
            #{main_window_obj_name} {{
                background-color: {MAIN_WINDOW_BG_COLOR};
            }}
            """
        )

        self.input_username = None
        self.input_phone = None
        self.run_button = None
        self.init_layouts()

        self.init_window_position(height=height, width=width)

        self.overlay_window = None
        self.thread_lightroom_automation = None
        self.thread_lightroom_launcher = None

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

    def init_layouts(self):
        main_central_layout = QVBoxLayout()

        self.init_input_main_fields(layout=main_central_layout)

        self.run_button = btn_run_main()
        self.run_button.clicked.connect(self.run_main_window)
        main_central_layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(main_central_layout)
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

    def init_threads(self):
        self.thread_lightroom_launcher = LightroomLaunchThread()
        self.thread_lightroom_automation = LightroomAutomationThread()

        self.thread_lightroom_launcher.launch_start.connect(
            self.on_lightroom_launcher_start
        )

        self.thread_lightroom_automation.automation.connect(
            self.on_lightroom_automation_finished
        )

    def run_main_window(self):
        self.init_threads()

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

            self.thread_lightroom_launcher.start()

        except Exception as e:
            log_exception_to_file(
                exception_obj=e,
                message="메인 윈도우에서 run_main_window 실행 중 에러발생",
            )

    def create_overlay(self):
        """독립적인 오버레이 창을 생성하고 부모 윈도우와 시그널 연결"""
        if self.overlay_window is not None:
            print("이미 오버레이가 생성 중입니다.")
            return

        self.overlay_window = OverlayWindow()  #  독립적인 오버레이 생성
        self.overlay_window.show()

    def on_lightroom_launcher_start(self, info: TypeSignalStatus):
        if info["status"] is False:
            self.show_guide_msg(
                msg_code=SIGNAL_LIGHTROOM_LAUHCNER_START_FAILED, info=info
            )
            self.cleanup_resources()
            return

        self.setWindowState(Qt.WindowMinimized)
        self.create_overlay()

        self.thread_lightroom_automation.start()

    def on_lightroom_automation_finished(self, info: TypeSignalStatus):

        self.raise_()  # ✅ 메인 윈도우를 최상위로 올림
        self.activateWindow()  # ✅ 메인 윈도우에 포커스 활성화

        if info["status"] is False:

            self.show_guide_msg(
                msg_code=info["status_code"], signal_info_msg=info["message"], info=info
            )
        else:
            show_guide(
                parent=self,
                file_path="메시지/안내메세지.txt",
                defalut_message="촬영 준비가 성공적으로 끝났습니다.",
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

    def show_guide_msg(self, msg_code="", signal_info_msg="", info=None):
        if msg_code == CAMERA_NOT_DETECTED:
            show_guide(parent=self, file_path="메시지/카메라감지실패메시지.txt")
        elif msg_code == CAMERA_NOT_SEARCHED:
            show_guide(parent=self, file_path="메시지/카메라감지실패메시지.txt")
        elif msg_code == AUTOMATION_APPLICATOIN_INIT_FAILED:
            show_guide(
                parent=self,
                file_path="",
                defalut_message="⚠️⚠️⚠️ 라이트룸을 다시 실행해주세요.",
            )
        elif msg_code == AUTOMATION_LIGHTROOM_FOCUS_FAILED_WITH_NOTE:
            show_guide(
                parent=self,
                file_path="",
                defalut_message="⚠️⚠️⚠️ 라이트룸의 모든 창을 닫고 프로그램을 다시 실행해주세요.",
            )

        else:
            error_msg_box = create_error_msg(
                parent=self, content=signal_info_msg, info=info
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
