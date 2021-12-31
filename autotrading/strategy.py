class Strategy:
    """
    매매 전략의 큰 그림
    매매 전략은 다음 두 가지로 구성
    1. 예비 신호
    2. 매매 계획
      2-1. 시장에 진입하는 기준
      2-2. 손절매 기준
      2-3. Add-up 기준
      2-4. 이익 실현을 위한 청산 기준
    """

    def __init__(self) -> None:
        self.name = ''  # 전략 이름

    def ready_signal(self):
        pass

    def entry(self):
        pass

    def stop_loss(self):
        pass

    def add_up(self):
        pass

    def exit(self):
        pass
