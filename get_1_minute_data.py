import os
import datetime
from config.setting import *
from autotrading.data.collector import UpbitCollector
from autotrading.machine.upbit_machine import QuotationAPI

collector = UpbitCollector(QuotationAPI)

upbit_market_code = collector.get_market_code()
print(upbit_market_code)