from pydantic import BaseModel
from threading import Lock
from rx.subject import BehaviorSubject


class AppState(BaseModel):
    """전역 상태 모델 (Lightroom 자동 제어를 위한 데이터 관리)"""
    username: str = ""  # 사용자가 입력한 이름
    phone_number: str = ""
    label_text: str = ""  # Label 텍스트 저장
    lightroom_running: bool = False  # Lightroom 실행 여부
    overlay_running: bool = False # 오버레이 실행 여부
    context: str = ""



class StateManager:
    """싱글톤 패턴 + ReactiveX(RxPy)를 활용한 전역 상태 관리자"""
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(StateManager, cls).__new__(cls)
                    cls._instance.state = BehaviorSubject(AppState())  # 상태 변경을 RxPy로 감지 가능
        return cls._instance

    def get_state(self) -> AppState:
        """현재 상태 반환"""
        return self.state.value

    def update_state(self, **kwargs):
        """상태 업데이트 (옵저버 패턴 적용)"""
        new_state = self.get_state().copy(update=kwargs)
        self.state.on_next(new_state)  # RxPy 이벤트 발생 (구독자에게 변경 사항 전달)

    def subscribe(self, callback):
        """상태 변경 감지 (RxPy 옵저버 패턴 적용)"""
        return self.state.subscribe(lambda new_state: callback(new_state))

    def reset_state(self):
        """기본 상태로 리셋"""
        self.state.on_next(AppState())
