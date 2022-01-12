from autotrading.machine.upbit_machine import *
import pandas as pd
import numpy as np


class MoneyManagement:

    def __init__(self, machine):
        self.machine = machine()
        self.account = self.set_account()

    def set_account(self):
        df = pd.DataFrame()
        accounts = self.machine.get_accounts()
        for account in accounts:
            df = df.append(account, ignore_index=True)

        return df


class AssetFixedMoneyManagement(MoneyManagement):
    def __init__(self, fixed_asset):
        super().__init__()
        self.fixed_asset_per_volume = fixed_asset
        self.available_trading_volume = self.set_available_trading_volume()

    def set_available_trading_volume(self):
        return int(float(self.account.iat[0, 1])) // self.fixed_asset_per_volume

    def get_available_trading_asset(self):
        return

    def get_available_trading_price(self):
        return


class RatioFixedMoneyManagement(MoneyManagement):
    pass


class TradingTimesFixedMoneyManagement(MoneyManagement):
    pass


class WilliamRiskFixedMoneyManagement(MoneyManagement):
    pass


class RiskRatioFixedMoneyManagement(MoneyManagement):
    pass


class VolatilityFixedMoneyManagement(MoneyManagement):
    pass
