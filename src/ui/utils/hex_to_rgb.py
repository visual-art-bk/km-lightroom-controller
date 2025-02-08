def hex_to_rgb(hex_color):
    """HEX 색상을 RGB 값으로 변환"""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 6:
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )
    return 0, 0, 255  # 기본값 BLUE
