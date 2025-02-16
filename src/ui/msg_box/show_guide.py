import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QMessageBox
from helpers.log_exception_to_file import log_exception_to_file


def show_guide(parent):
    file_path = "안내메세지.txt"  # 루트 디렉토리에 있는 파일

    try:
        # 파일에서 메시지 읽기
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                message_text = file.read().strip()
        else:
            message_text = "⚠️ 중요 안내: 계속 진행하시겠습니까?"

        # 메시지 박스 생성 및 표시
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("확인 필요")
        msg_box.setText(message_text)

        # 이 부분을 적용해야 메모장의 콘텐트 너비로 적용된 값으로 
        # 박스 너비를 새로고침하고
        # 그래야 하단의 박스 정중앙 위치 값에 올바른 값을 참조할 수 있다
        msg_box.adjustSize()

        msg_box.setStandardButtons(QMessageBox.Ok)

        # 메시지 박스 상하좌우 가운데 정렬
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        msg_box_width = msg_box.width()
        msg_box_height = msg_box.height()

        x = (screen_width - msg_box_width) // 2
        y = (screen_height - msg_box_height) // 2

        msg_box.move(x, y)

        # 사용자의 선택을 반환
        return msg_box.exec() == QMessageBox.Ok

    except Exception as e:
        parent.show_err_msg()
        log_exception_to_file(
            exception_obj=e, message="메모장 파일을 읽는 중 오류 발생"
        )
        return False 
