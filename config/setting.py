import configparser

parser = configparser.ConfigParser()
parser.read('config/config.ini')

UPBIT_ACCESS_KEY = parser.get('upbit', 'access_key')
UPBIT_SECRET_KEY = parser.get('upbit', 'secret_key')
DIR_UPBIT_DATABASE = 'D:\\coin_database\\domestic\\upbit'
DIR_UPBIT_DAILY_CANDLE = DIR_UPBIT_DATABASE + '\\daily'
DIR_UPBIT_MINUTELY_CANDLE = DIR_UPBIT_DATABASE + '\\minutely'
DIR_UPBIT_DATABASE_BACKUP = 'E:\\backup\\coin_database\\domestic\\upbit'
DIR_UPBIT_DAILY_CANDLE_BACKUP = DIR_UPBIT_DATABASE_BACKUP + '\\daily'
DIR_UPBIT_MINUTELY_CANDLE_BACKUP = DIR_UPBIT_DATABASE_BACKUP + '\\minutely'

# BITHUMB_CONNECT_KEY = parser.get('bithumb', 'connect_key')
# BITHUMB_SECRET_KEY = parser.get('bithumb', 'secret_key')
# DIR_BITHUMB_DATABASE = 'D:\\coin_database\\domestic\\bithumb'
# DIR_BITHUMB_DAILY_CANDLE = DIR_BITHUMB_DATABASE + '\\daily'
# DIR_BITHUMB_MINUTELY_CANDLE = DIR_BITHUMB_DATABASE + '\\minutely'
# DIR_BITHUMB_DATABASE_BACKUP = 'E:\\backup\\coin_database\\domestic\\bithumb'
# DIR_BITHUMB_DAILY_CANDLE_BACKUP = DIR_BITHUMB_DATABASE_BACKUP + '\\daily'
# DIR_BITHUMB_MINUTELY_CANDLE_BACKUP = DIR_BITHUMB_DATABASE_BACKUP + '\\minutely'

# KORBIT_CLIENT_ID = parser.get('korbit', 'client_id')
# KORBIT_CLIENT_SECRET = parser.get('korbit', 'client_secret')
# DIR_KORBIT_DATABASE = 'D:\\coin_database\\domestic\\korbit'
# DIR_KORBIT_DAILY_CANDLE = DIR_KORBIT_DATABASE + '\\daily'
# DIR_KORBIT_MINUTELY_CANDLE = DIR_KORBIT_DATABASE + '\\minutely'
# DIR_KORBIT_DATABASE_BACKUP = 'E:\\backup\\coin_database\\domestic\\korbit'
# DIR_KORBIT_DAILY_CANDLE_BACKUP = DIR_KORBIT_DATABASE_BACKUP + '\\daily'
# DIR_KORBIT_MINUTELY_CANDLE_BACKUP = DIR_KORBIT_DATABASE_BACKUP + '\\minutely'

# COINONE_ACCESS_TOKEN = parser.get('coinone', 'access_token')
# COINONE_SECRET_KEY = parser.get('coinone', 'secret_key')
# DIR_COINONE_DATABASE = 'D:\\coin_database\\domestic\\coinone'
# DIR_COINONE_DAILY_CANDLE = DIR_COINONE_DATABASE + '\\daily'
# DIR_COINONE_MINUTELY_CANDLE = DIR_COINONE_DATABASE + '\\minutely'
# DIR_COINONE_DATABASE_BACKUP = 'E:\\backup\\coin_database\\domestic\\coinone'
# DIR_COINONE_DAILY_CANDLE_BACKUP = DIR_COINONE_DATABASE_BACKUP + '\\daily'
# DIR_COINONE_MINUTELY_CANDLE_BACKUP = DIR_COINONE_DATABASE_BACKUP + '\\minutely'
