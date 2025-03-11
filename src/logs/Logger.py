import os
import sys
import logging
from logging.handlers import RotatingFileHandler


class Logger:
    """📌 파일 및 콘솔에 로그를 기록하는 클래스 (2025년 업계 표준 적용)"""

    def __init__(self, log_filename="app_log.txt", max_log_size=1_000_000, backup_count=3):
        """
        Logger 클래스 생성자
        :param log_filename: 로그 파일 이름
        :param max_log_size: 최대 로그 파일 크기 (bytes)
        :param backup_count: 보관할 백업 로그 파일 개수
        """
        # ✅ 실행 중인 파일(.exe 또는 .py)의 위치 가져오기
        exe_path = sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__)
        exe_dir = os.path.dirname(exe_path)  # 실행 파일 폴더
        self.log_file_path = os.path.join(exe_dir, log_filename)  # 로그 파일 경로

        # ✅ Logger 설정
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.DEBUG)  # DEBUG 레벨부터 기록 가능하도록 설정

        # ✅ 로그 포맷 정의
        log_format = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # ✅ 로그 파일 핸들러 (파일 크기가 초과되면 순환)
        file_handler = RotatingFileHandler(
            self.log_file_path, maxBytes=max_log_size, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)  # 모든 로그 기록 가능
        file_handler.setFormatter(log_format)

        # ✅ 콘솔 핸들러 (표준 출력)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_format)

        # ✅ 핸들러 추가
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        """✅ 일반 로그 기록 (INFO)"""
        self.logger.info(message)

    def error(self, message, exception_obj=None):
        """🚨 오류 및 예외 발생 시 상세 로그 기록 (ERROR)"""
        if exception_obj:
            self.logger.exception(message)  # ✅ traceback 자동 포함
        else:
            self.logger.error(message)