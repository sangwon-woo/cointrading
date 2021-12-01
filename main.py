import configparser 
import pybithumb

parser = configparser.ConfigParser()
parser.read('config/config.ini')

connect_key = parser.get('bithumb', 'connect_key')
secret_key = parser.get('bithumb', 'secret_key')

bithumb = pybithumb.Bithumb(connect_key, secret_key)

balance = bithumb.get_balance('BTC')

