from typing import TypedDict

class TypeAutomationSignal(TypedDict):
    """Lightroom 자동화 시그널 데이터 타입"""
    status: bool
    message: str
    error_code: str