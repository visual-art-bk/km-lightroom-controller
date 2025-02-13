from ui.utils.hex_to_rgb import hex_to_rgb

def apply_bg_wideg_style(bg_color, opacity, target="#overlayContainer"):
    """✅ 특정 요소(ID 또는 클래스)에만 배경색과 투명도를 적용"""
    r, g, b = hex_to_rgb(bg_color)

    # ✅ ID 또는 클래스에만 적용하는 스타일
    style = f"""
        {target} {{
            background-color: rgba({r}, {g}, {b}, {opacity});
            border-radius: 20px;  /* ✅ 원하는 보더 라운드 값 설정 */
            border: 2px solid black;
        }}
    """
    return style
