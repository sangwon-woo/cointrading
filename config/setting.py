import configparser

parser = configparser.ConfigParser()
parser.read('config/config.ini')

UPBIT_ACCESS_KEY = parser.get('upbit', 'access_key')
UPBIT_SECRET_KEY = parser.get('upbit', 'secret_key')
DIR_UPBIT_DATABASE = 'D:\\coin_database\\domestic\\upbit'
DIR_UPBIT_DAILY_CANDLE = DIR_UPBIT_DATABASE + '\\daily'
DIR_UPBIT_MINUTELY_CANDLE = DIR_UPBIT_DATABASE + '\\minutely'

BITHUMB_CONNECT_KEY = parser.get('bithumb', 'connect_key')
BITHUMB_SECRET_KEY = parser.get('bithumb', 'secret_key')
BITHUMB_DATABASE_DIR = 'D:\\coin_database\\domestic\\bithumb'

KORBIT_CLIENT_ID = parser.get('korbit', 'client_id')
KORBIT_CLIENT_SECRET = parser.get('korbit', 'client_secret')
KORBIT_DATABASE_DIR = 'D:\\coin_database\\domestic\\korbit'

COINONE_ACCESS_TOKEN = parser.get('coinone', 'access_token')
COINONE_SECRET_KEY = parser.get('coinone', 'secret_key')
COINONE_DATABASE_DIR = 'D:\\coin_database\\domestic\\coinone'



