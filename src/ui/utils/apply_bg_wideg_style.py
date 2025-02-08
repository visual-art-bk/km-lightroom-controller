from ui.utils.hex_to_rgb import hex_to_rgb


def apply_bg_wideg_style(bg_color, opacity):
    """✅ 배경색과 투명도를 `rgba()`로 강력하게 적용"""
    r, g, b = hex_to_rgb(bg_color)

    # ✅ rgba()를 사용하여 배경색과 투명도를 동시에 적용
    style = f"""
            background-color: rgba({r}, {g}, {b}, {opacity * 255});
            border-radius: 20px;  /* ✅ 원하는 보더 라운드 값 설정 */
            border: 2px solid black;
        """

    return style
