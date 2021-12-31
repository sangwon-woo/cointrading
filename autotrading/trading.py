class Trading:
    """
    One Trading에 대한 큰 그림
    한 번의 트레이딩은 다음과 같은 것들을 포함해야 한다.
    . 매매전략
    . 시장
    . 종목
    . 포지션 방향(Long, Short)
    . 포지션 사이즈(진입가격 * 매매수량)
    . 진입시점
    . 진입가격
    . 진입수량
    . 청산시점
    . 청산가격
    . 청산수량
    . 수익률
    """

    def __init__(self, strategy, market, item) -> None:
        self.strategy = strategy  # 매매전략
        self.market = market  # 시장
        self.item = item  # 종목
        self.position = ''  # 포지션 방향
        self.gross_position_size = 0  # 총 포지션 사이즈
        self.net_position_size = 0  # 순수 포지션 사이즈
        self.entry_datetime = []  # 진입시점
        self.entry_price = []  # 진입가격
        self.entry_volume = []  # 진입수량
        self.exit_datetime = []  # 청산시점
        self.exit_price = []  # 청산가격
        self.exit_volume = []  # 청산수량
        self.gross_profit_loss = 0  # 총손익
        self.trading_cost = 0  # 거래비용
        self.net_profit_loss = 0  # 순손익

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def update_entry_data(self, trade_time, price, volume):
        self.entry_datetime.append(trade_time)
        self.entry_price.append(price)
        self.entry_volume.append(volume)
