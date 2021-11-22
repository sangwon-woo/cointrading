from base_machine import Machine
import configparser

class KorbitMachine:
    """
    코빗 거래소와의 거래를 위한 클래스
    BASE_API_URL은 API 호출을 위한 기본 URL
    TRADE_CURRENCY_TYPE은 코빗에서 거래가 가능한 화폐의 종류
    """
    BASE_API_URL = "https://api.korbit.co.kr"
    TRADE_CURRENCY_TYPE = ['btc', 'bch', 'btg', 'eth', 'etc', 'xrp', 'krw']

    def __init__(self) -> None:
        """
        KorbitMahcine 클래스에서 가장 먼저 호출되는 메서드
        config.ini에서 client_id, client_secret, username, password 정보를 읽어옴
        """
        config = configparser.ConfigParser()
        config.read('conf/config.ini')

        self.CLIENT_ID = config['KORBIT']['client_id']
        self.CLIENT_SECRET = config['KORBIT']['client_secret']
        self.USER_NAME = config['KORBIT']['username']
        self.PASSWORD = config['KORBIT']['password']
        self.access_token = None
        self.refresh_token = None
        self.token_type = None


if __name__ == '__main__':
    korbit = KorbitMachine()
    print(korbit.CLIENT_ID, korbit.CLIENT_SECRET, korbit.USER_NAME, korbit.PASSWORD, sep='\n')