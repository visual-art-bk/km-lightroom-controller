import os
import shutil
import subprocess

# PyInstaller 빌드 실행
subprocess.run([
    "pyinstaller", "--onedir", "--noupx", "--name=다비 촬영 매니저",
    "--noconsole", "--noconfirm", "--clean",
    "--hidden-import=PySide6",
    "--hidden-import=pywinauto",
    "src/main.py"
], check=True)

# 빌드된 실행 파일이 위치할 폴더
exe_dir = "dist/다비 촬영 매니저"

# 복사할 폴더 목록
folders_to_copy = ["메시지", "assets"]

for folder in folders_to_copy:
    source_dir = folder
    destination_dir = os.path.join(exe_dir, folder)

    if os.path.exists(source_dir):
        shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
        print(f"{folder} 폴더가 {destination_dir}로 복사되었습니다.")
    else:
        print(f"{folder} 폴더가 존재하지 않습니다!")

# ✅ 설정.yaml 파일 복사 추가
config_file = "설정.yaml"  # 루트에 있는 설정 파일명

if os.path.exists(config_file):
    shutil.copy(config_file, exe_dir)
    print(f"✅ 설정 파일 '{config_file}'이(가) {exe_dir}로 복사되었습니다.")
else:
    print(f"⚠️ 설정 파일 '{config_file}'이(가) 존재하지 않습니다!")
