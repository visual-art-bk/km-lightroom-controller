def move_msg_center(parent, msg_box):
    # ✅ 화면 정중앙에 메시지 박스를 배치
    if parent.isVisible():  # 메인 윈도우가 존재하면
        parent_geometry = parent.frameGeometry()
        msg_box_geometry = msg_box.frameGeometry()
        msg_box_geometry.moveCenter(
            parent_geometry.center()
        )  # 메인 윈도우 중앙 좌표로 이동
        msg_box.move(msg_box_geometry.topLeft())  # 최종 이동
    else:  # 메인 윈도우가 보이지 않는다면, 화면 정중앙에 배치
        screen_geometry = msg_box.screen().availableGeometry()
        msg_box_geometry = msg_box.frameGeometry()
        msg_box_geometry.moveCenter(screen_geometry.center())  # 전체 화면 중앙 좌표
        msg_box.move(msg_box_geometry.topLeft())
