from typing import TypedDict, Optional

class TypeAutomationSignal(TypedDict):
    """Lightroom 자동화 시그널 데이터 타입"""
    status: bool
    message: str
    error_code: str

class TypeSignalStatus(TypedDict):
    status: bool
    status_code: str
    message: Optional[str]