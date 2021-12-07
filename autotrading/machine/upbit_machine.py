import requests
import config.setting as st

class UpbitMachine:
    """
    업비트 거래소와의 거래를 위한 클래스
    BASE_API_URL은 API 호출을 위한 기본 URL
    """

    BASE_API_URL = 'https://api.upbit.com/v1'

    def __init__(self) -> None:
        self.ACCESS_KEY = st.UPBIT_ACCESS_KEY
        self.SECRET_KEY = st.UPBIT_SECRET_KEY
        self.DATABASE_DIR = st.UPBIT_DATABASE_DIR
        self.access_token = None
        self.refresh_token = None


class ExchangeAPI(UpbitMachine):
    """
    업비트 API 중 Exchange와 관련된 API
    1. 자산
        - 전체 계좌 조회 : 내가 보유한 자산 리스트 조회
    2. 주문
        - 주문 가능 정보 조회 : 마켓별 주문 가능 정보를 확인
        - 개별 주문 조회 : 주문 UUID를 통해 개별 주문건을 조회
        - 주문 리스트 조회 : 주문 리스트 조회
        - 주문 취소 접수 : 주문 UUID를 통해 해당 주문에 대한 취소 접수
        - 주문하기 : 주문 요청
    3. 입금
        - 전체 입금 주소 조회 : 나의 전체 입금 주소 조회
        - 개별 입금 주소 조회 : 특정 화폐의 입금 주소 조회
        - 개별 입금 조회 : 입금 UUID를 통해 개별 입금건을 조회
        - 입금 리스트 조회 : 입금 리스트 조회
        - 입금 주소 생성 요청 : 입금 주소 생성 요청
        - 원화 입금하기 : 원화 입금 요청
    4. 출금
        - 출금 가능 정보 조회 : 해당 통화의 가능한 출금 정보를 확인
        - 개별 출금 조회 : 출금 UUID를 통해 개별 출금 정보 조회
        - 출금 리스트 조회 : 출금 리스트 조회
        - 코인 출금하기 : 코인 출금 요청
        - 원화 출금하기 : 원화 출금 요청, 등록된 출금 계좌로 출금
    5. 서비스 정보
        - 입출금 현황 : 입출금 현황 및 블록 상태 조회
        - API 키 리스트 조회 : API 키 목록 및 만료 일자 조회
    """
    def __init__(self) -> None:
        super().__init__()
        

class QuotationAPI:
    def __init__(self) -> None:
        pass

