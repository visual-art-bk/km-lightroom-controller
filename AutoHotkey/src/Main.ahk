#Requires AutoHotkey v2.0+

LIGHTROOM_EXE := "Lightroom.exe"
LIGHTROOM_PATH := "C:\Program Files\Adobe\Adobe Lightroom Classic\Lightroom.exe"
WINDOW_TITLE := "Lightroom"  ; 창 제목

; Lightroom Classic 파일 메뉴 열기
SetTitleMatchMode "2"  ; 창 제목 매칭 모드 설정 (부분 일치 허용)

Run(LIGHTROOM_PATH)

Sleep(3000)

Send "!f"  ; Alt + F 입력 (파일 메뉴 열기)