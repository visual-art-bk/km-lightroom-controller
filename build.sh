#!/bin/bash

# PyInstaller 빌드 실행
pyinstaller --onedir --noupx --name="LightroomController" \
    --noconsole --noconfirm --clean \
    --hidden-import=PySide6 \
    --hidden-import=pywinauto \
    src/main.py