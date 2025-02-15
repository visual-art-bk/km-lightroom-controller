import os
from PySide6.QtCore import Qt
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
        msg_box.setStandardButtons(QMessageBox.Ok)

        # ✅ 메시지 창을 최상위로 고정
        msg_box.setWindowModality(Qt.ApplicationModal)  # 부모 창을 블러킹 (다른 창 못 누름)
        msg_box.raise_()  # 최상위로 올리기
        msg_box.activateWindow()  # 포커스 활성화

        return msg_box.exec() == QMessageBox.Ok  # 사용자의 선택 반환

    except Exception as e:
        parent.show_err_msg()
        log_exception_to_file(
            exception_obj=e, message="메모장 파일을 읽는 중 오류 발생"
        )
        return False
