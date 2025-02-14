from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from .move_msg_center import move_msg_center

def create_done_msg(parent):
    msg_box = QMessageBox(
        parent
    )  # ✅ 부모 윈도우 설정 (현재 윈도우가 닫혀도 메시지박스 유지)
    msg_box.setIcon(QMessageBox.Icon.Information)  # ℹ️ 정보 아이콘 설정
    msg_box.setWindowTitle("알림")  # 창 제목
    msg_box.setText(
        "📸 내보내기가 시작됐어요!\n\n"
        "⏳ 약 10분 정도 소요됩니다.\n\n"
        "✅ '확인' 버튼을 눌러주시고,\n"
        "🎨 촬영 소품, 배경지, 리모컨을 정리한 후\n"
        "🚶‍♂️ 셀렉실로 이동해주세요."
    )  # 메시지 내용

    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)  # "확인" 버튼 추가

    # ✅ 메시지 박스를 항상 최상위 창으로 설정
    msg_box.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)

    # ✅ 메시지 박스를 먼저 띄운 후 크기 확정
    msg_box.adjustSize()  # 크기를 자동으로 조정
    msg_box.show()  # 크기를 확정하기 위해 먼저 표시
    msg_box.repaint()  # UI 갱신 (위치 보정)

    move_msg_center(parent=parent, msg_box=msg_box)

    return msg_box
