"""
위험관리는 One Trading에 총(계좌)자산의 몇 %의 리스크를 부담할 것인가. 

"""

class RiskManagement:
    def __init__(self) -> None:
        self.total_asset = 0
        self.risk_percentage = 0

    def set_total_asset(self, total_asset):
        self.total_asset = total_asset

    def set_risk_percentage(self, risk_percentage):
        assert risk_percentage in [1, 2, 3], "Select box : 1%, 2%, 3%"
        self.risk_percentage = risk_percentage

    