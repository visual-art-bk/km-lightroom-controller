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
from ui.inputs.input_main_field import input_main_field
from ui.inputs.input_container import input_container
from ui.buttons.btn_run_main import btn_run_main
from ui.msg_box.show_guide import show_guide
from ui.surfaces import create_shadow_widget, create_central_widget
from ui.effects import create_shadow_effect


class MainWindow(QMainWindow):
    def __init__(self, x=None, y=0, width=MAIN_WINDOW_WIDTH, height=MAIN_WINDOW_HEIGHT):
        super().__init__()

        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        size_dict: SizeDict = {
            "width": width,
            "height": height,
            "screen_width": screen_width,
            "screen_height": screen_height,
        }

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.init_surface_widgets(size=size_dict)

        self.init_layouts(mainWidget=self.mainWidget)

        self.setCentralWidget(self.mainContainerWidget)

        self.init_window_position(height=height, width=width)

        self.overlay_window = None
        self.thread_lightroom_automation = None

        self.init_state_manager()

    def init_surface_widgets(self, size: SizeDict):
        width = size.get("width")
        height = size.get("height")

        self.mainContainerWidget = QWidget(self)
        self.mainContainerWidget.setGeometry(0, 0, width, height)

        self.shadowWidget = create_shadow_widget(size=size)
        self.shadowWidget.setParent(self.mainContainerWidget)

        self.mainWidget = create_central_widget(size=size)
        self.mainWidget.setParent(self.mainContainerWidget)

    def init_top_app_bar_layout(self):
        style = """
            background-color: red;
        """
        layout = QHBoxLayout()

        test_widget = QWidget()
        test_widget.setFixedSize(50, 50)
        test_widget.setStyleSheet(style)

        test_widget_2 = QWidget()
        test_widget_2.setFixedSize(50, 50)
        test_widget_2.setStyleSheet(style)
        layout.setSpacing(10)
        layout.addWidget(test_widget)
        layout.addWidget(test_widget_2)

        return layout

    def init_display_layout(self):
        style = """
            background-color: yellow;
        """
        display = QWidget()

        display.setStyleSheet(style)

        display.setFixedWidth(300)
        display.setFixedHeight(300)  # 원하는 높이로 설정 (예: 300px)

        layout = QHBoxLayout()
        layout.addWidget(display)

        return layout

    def init_inputs_layout(self):
        self.inputUsernNameWidget = input_container(
            label="예약자 성함", placeholder="예) 홍길동"
        )
        self.inputPhoneNumberWidget = input_container(
            label="전화번호 뒷 4자리",
            placeholder="예) 1234",
        )
        layout = QVBoxLayout()

        layout.addWidget(self.inputUsernNameWidget)
        layout.addWidget(self.inputPhoneNumberWidget)

        layout.setSpacing(20)
        layout.addStretch()
        layout.setContentsMargins(8, 24, 8, 0)

        return layout

    def toggle_run_btn_icon(self, is_started=False):
        if is_started:
            self.run_button.setIcon(self.run_btn_stop_icon)
            print("▶ → ■ 변경됨: 실행 중")

        else:
            self.run_button.setIcon(self.run_btn_play_icon)
            print("■ → ▶ 변경됨: 정지됨")

    def init_run_btn_layout(self):
        self.run_btn_play_icon = QIcon(RUN_BTN_PLAY_ICON_PATH)
        self.run_btn_stop_icon = QIcon(RUN_BTN_STOP_ICON_PATH)

        self.run_button = QPushButton()
        self.run_button.setIcon(self.run_btn_play_icon)
        self.run_button.setIconSize(QSize(40, 40))
        self.run_button.setFixedSize(40, 40)

        self.run_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.run_button.clicked.connect(self.run_main_window)

        layout = QHBoxLayout()
        layout.addWidget(self.run_button)
        layout.setContentsMargins(0, 0, 0, 24)
        layout.setSpacing(48)

        return layout

    def init_layouts(self, mainWidget):
        main_central_layout = QVBoxLayout(mainWidget)
        main_central_layout.setContentsMargins(0, 0, 0, 0)

        top_app_bar_layout = self.init_top_app_bar_layout()
        display_layout = self.init_display_layout()
        inputs_layout = self.init_inputs_layout()
        run_btn_layout = self.init_run_btn_layout()

        main_central_layout.addLayout(top_app_bar_layout)
        main_central_layout.addLayout(display_layout)
        main_central_layout.addLayout(inputs_layout)
        main_central_layout.addLayout(run_btn_layout)

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
            username = self.inputUsernNameWidget.inputEntry.text().strip()
            phone_number = self.inputPhoneNumberWidget.inputEntry.text().strip()

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
            self.toggle_run_btn_icon(is_started=True)

            QTimer.singleShot(1500, self.delayed_tasks_after_start)

        except Exception as e:
            log_exception_to_file(
                exception_obj=e,
                message="메인 윈도우에서 run_main_window 실행 중 에러발생생",
            )

    def delayed_tasks_after_start(self):
        """Lightroom 스레드 실행 및 UI 상태 업데이트"""
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
