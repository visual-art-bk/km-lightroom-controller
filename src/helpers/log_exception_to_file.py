import os
import sys
import time
import traceback

def log_exception_to_file(message, exception_obj=None, log_filename="error_log.txt", max_log_size=1_000_000):
    """✅ 예외 발생 시 실행 파일이 있는 폴더에 로그를 저장하는 함수"""

    try:
        # ✅ 실행 중인 파일(.exe 또는 .py)의 위치 가져오기
        exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        exe_dir = os.path.dirname(exe_path)  # 실행 파일 폴더
        log_file_path = os.path.join(exe_dir, log_filename)  # 로그 파일 경로

        # ✅ 로그 파일이 1MB 초과하면 삭제
        if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > max_log_size:
            try:
                os.remove(log_file_path)  # 파일 삭제
                print(f"🗑️ 로그 파일이 1MB를 초과하여 삭제됨: {log_file_path}")
            except Exception as e:
                print(f"❌ 로그 파일 삭제 실패: {e}")

        # ✅ 로그 파일 기록
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write("\n" + "=" * 60 + "\n")
            log_file.write(f"📌 [오류 발생 시각]: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write("=" * 60 + "\n")
            log_file.write(message + "\n")

            if exception_obj:
                log_file.write("\n🔍 [Traceback Details]:\n")
                log_file.write(traceback.format_exc())  # 자세한 traceback 정보 추가

            log_file.write("\n" + "=" * 60 + "\n\n")

        print(f"🚨 오류가 발생하여 {log_file_path} 에 저장되었습니다.")

    except Exception as e:
        print(f"❌ 로그 파일 기록 실패: {e}")
