import configparser 
import pybithumb
import pyupbit

parser = configparser.ConfigParser()
parser.read('config/config.ini')

connect_key = parser.get('bithumb', 'connect_key')
secret_key = parser.get('bithumb', 'secret_key')

bithumb = pybithumb.Bithumb(connect_key, secret_key)

balance = bithumb.get_balance('BTC')

acc_key = parser.get('upbit', 'access_key')
sec_key = parser.get('upbit', 'secret_key')

upbit = pyupbit.Upbit(acc_key, sec_key)
upbit_balance = upbit.get_balances()
print(upbit_balance)