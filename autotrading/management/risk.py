from autotrading.machine.upbit_machine import *

ex = ExchangeAPI()
res = ex.get_accounts()
print(res)
