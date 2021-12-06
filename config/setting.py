import configparser

parser = configparser.ConfigParser()
parser.read('config/config.ini')

UPBIT_ACCESS_KEY = parser.get('upbit', 'access_key')
UPBIT_SECRET_KEY = parser.get('upbit', 'secret_key')



