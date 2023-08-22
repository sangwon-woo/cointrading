"""
upbit machine
"""

import time
import json
import uuid
import hashlib
import jwt
import websockets
import pandas as pd
import requests as rq
import config.setting as st
from multiprocessing import Process
from urllib.parse import urlencode
import asyncio


class UpbitMachine:
    """
    업비트 거래소와의 거래를 위한 클래스
    BASE_API_URL은 API 호출을 위한 기본 URL
    """

    BASE_API_URL = 'https://api.upbit.com/v1'

    def __init__(self) -> None:
        self.ACCESS_KEY = st.UPBIT_ACCESS_KEY
        self.SECRET_KEY = st.UPBIT_SECRET_KEY
        self.DIR_DATABASE = st.DIR_UPBIT_DATABASE
        self.access_token = None
        self.refresh_token = None


class ExchangeAPI(UpbitMachine):
    """
    업비트 API 중 Exchange와 관련된 API
    --------

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

    def get_headers(self, query_string):
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': self.ACCESS_KEY,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512'
        }

        jwt_token = jwt.encode(payload, self.SECRET_KEY)
        authorize_token = f'Bearer {jwt_token}'
        headers = {"Authorization": authorize_token}

        return headers

    def get_accounts(self):
        """
        내가 보유한 자산 리스트 조회
        """

        url = self.BASE_API_URL + '/accounts'
        payload = {
            'access_key': self.ACCESS_KEY,
            'nonce': str(uuid.uuid4())
        }

        jwt_token = jwt.encode(payload, self.SECRET_KEY)
        authorization_token = f'Bearer {jwt_token}'
        headers = {'Authorization': authorization_token}

        res = rq.get(url, headers=headers).json()

        return res

    def get_orders_chance(self, market: str = 'KRW-BTC'):
        """
        마켓별 주문 가능 정보를 확인

        Parameters
        ----------
        market : str
            마켓 ID. 기본값은 KRW-BTC
        """

        url = self.BASE_API_URL + '/orders/chance'
        query = {
            'market': market
        }
        query_string = urlencode(query).encode()

        headers = self.get_headers(query_string)

        res = rq.get(url, params=query, headers=headers).json()

        return res

    def get_order(self, uuid: str):
        """
        주문 UUID를 통해 개별 주문건을 조회

        Parameters
        ----------
        uuid : str
            주문 UUID
        """

        url = self.BASE_API_URL + '/order'
        query = {
            'uuid': uuid
        }
        query_string = urlencode(query).encode()

        headers = self.get_headers(query_string)

        res = rq.get(url, params=query, headers=headers).json()

        return res

    def get_order_list(self, uuids: list, **kwargs):
        """
        주문 UUID를 통해 개별 주문건을 조회

        Parameters
        ----------
        uuids : list
            주문 UUID의 목록
        kwargs : 
            market : str
                마켓 아이디
            state : str
                주문 상태. wait, watch, done, cancel
            states : list
                주문 상태의 목록. 미체결 주문(wait, watch)과 완료 주문(done, cancel)은 혼합하여 조회할 수 없음
            page : int
                페이지 수. 기본값은 1
            limit : int
                요청 개수. 기본값은 100
            order_by : str
                정렬 방식. asc(오름차순), desc(내림차순, 기본값)
        """

        url = self.BASE_API_URL + '/orders'
        query = kwargs
        query_string = urlencode(query)
        uuids_query_string = '&'.join([f'uuids[]={uuid}' for uuid in uuids])
        query_string = f'{query_string}&{uuids_query_string}'.encode()

        query['uuids[]'] = uuids

        headers = self.get_headers(query_string)

        res = rq.get(url, params=query, headers=headers)

        return res

    def delete_order(self, uuid: str):
        """
        주문 UUID를 통해 해당 주문에 대한 취소 접수

        Parameters
        ----------
        uuid : list
            취소할 주문의 UUID
        """
        url = self.BASE_API_URL + '/order'
        query = {
            'uuid': uuid
        }
        query_string = urlencode(query).encode()

        headers = self.get_headers(query_string)

        res = rq.delete(url, params=query, headers=headers).json()

        return res

    def post_order(self, market: str, side: str, volume: str, price: str, ord_type: str):
        """
        주문 요청

        Parameters
        ----------
        market : str
            마켓 ID
        side : str
            주문 종류. bid(매수), ask(매도)
        volume : str
            주문량. 지정가 및 시장가 매도 시 필수
        price : str
            주문 가격. 지정가 및 시장가 매수 시 필수
        ord_type : str
            주문 타입. limit(지정가 주문), price(시장가 매수 주문), market(시장가 매도 주문)
        """

        url = self.BASE_API_URL + '/orders'

        query = {
            'market': market,
            'side': side,
            'volume': volume,
            'price': price,
            'ord_type': ord_type
        }
        query_string = urlencode(query).encode()

        headers = self.get_headers(query_string)

        res = rq.post(url, params=query, headers=headers).json()

        return res

    def get_coin_addresses(self):
        pass

    def get_coin_address(self, currency, deposit_address, secondary_address):
        pass

    def get_deposit(self, uuid, txid, currency):
        pass

    def get_deposit_list(self, currency, state, uuids, txids, limit, page, order_by):
        pass

    def post_generate_coin_address(self, currency):
        pass

    def post_krw_deposit(self, amount):
        pass

    def get_withdraws_chance(self):
        pass

    def get_withdraw(self, uuid, txid, currency):
        pass

    def get_withdraw_list(self, currency, state, uuids, txids, limit, page, order_by):
        pass

    def post_coin_withdraw(self, currency, amount, address, secondary_address, transaction_type):
        pass

    def post_krw_withdraw(self, amount):
        pass

    def get_wallet_status(self):
        pass

    def get_api_keys(self):
        pass


class QuotationAPI(UpbitMachine):
    """
    업비트 API 중 Quotation과 관련된 API
    1. 시세 종목 조회
        - 마켓 코드 조회 : 업비트에서 거래 가능한 마켓 목록
    2. 시세 캔들 조회
        - 분 캔들 : 분 캔들 조회
        - 일 캔들 : 일 캔들 조회
        - 주 캔들 : 주 캔들 조회
        - 월 캔들 : 월 캔들 조회
    3. 시세 체결 조회
        - 최근 체결 내역 : 체결 내역 조회
    4. 시세 Ticker 조회
        - 현재가 정보 : 요청 당시 종목의 스냅샷 조회
    5. 시세 호가 정보 조회
        - 호가 정보 조회 : 요청 당시 종목의 호가 정보 조회(1호가부터 15호가까지)
    """

    def __init__(self) -> None:
        super().__init__()
        self.headers = {
            'Accept': 'application/json'
        }

    def get_market_code(self, is_details=False) -> pd.DataFrame:
        """
        업비트에서 거래 가능한 마켓 목록 조회

        Parameters
        ----------
        is_details : Bool
            유의종목 필드와 같은 상세 정보 노출 여부. 기본값은 False
        """
        df = pd.DataFrame()
        is_details = 'false' if is_details == False else 'true'
        url = self.BASE_API_URL + '/market/all?isDetails={}'.format(is_details)

        # try - except
        res = rq.get(url, headers=self.headers)
        time.sleep(0.1)

        return res

    def get_minute_candle(self, unit=1, market='KRW-BTC', to=None, count=1) -> pd.DataFrame:
        """
        특정 화폐의 분봉 조회
        ----------

        Parameters
        ----------
        unit : int
            분봉의 단위. 기본값은 1
            가능한 값 : 1, 3, 5, 10, 15, 30, 60, 240
        market : string
            마켓 코드. 기본값은 KRW-BTC
        to : string
            마지막 캔들 시각(exclusive). 기본값은 None 
            포맷 : yyyy-MM-dd HH:mm:ss
        count : int
            캔들 갯수. 기본값은 1. 최대 200개까지 요청 가능. 
        """
        df = pd.DataFrame()
        base_url = self.BASE_API_URL + '/candles/minutes/{}?'.format(unit)

        if to:
            print(f'{market} => {to}보다 이전 {unit}분봉 데이터 조회')
            to = to.replace(' ', '%20').replace(':', '%3A')
            query = 'market={}&to={}&count={}'.format(market, to, count)
        else:
            query = 'market={}&count={}'.format(market, count)

        url = base_url + query

        # try - except
        res = rq.get(url, headers=self.headers).json()
        time.sleep(0.1)

        return pd.DataFrame(res)

    def get_day_candle(self, market='KRW-BTC', to=None, count=1, converting_price_unit=None) -> pd.DataFrame:
        """
        특정 화폐의 일봉 조회

        Parameters
        ----------
        market : string
            마켓 코드. 기본값은 KRW-BTC
        to : string
            마지막 캔들 시각(exclusive). 기본값은 None
            포맷 : yyyy-MM-dd HH:mm:ss
        count : int
            캔들 갯수. 기본값은 1. 최대 200개까지 요청 가능. 
        converting_price_unit : string
            원화 마켓이 아닌 다른 마켓의 일봉 요청시 종가를 명시된 파라미터 값으로 환산. 기본값은 None.
            현재는 원화(KRW)로 변환하는 기능만 제공하며 추후 기능을 확장할 수 있음. 
        """
        df = pd.DataFrame()
        base_url = self.BASE_API_URL + '/candles/days?'

        if to:
            if converting_price_unit:
                print(
                    f'{market} => {to}보다 이전 일봉 데이터 및 {converting_price_unit}로 환산하여 조회')
                to = to.replace(' ', '%20').replace(':', '%3A')
                query = 'market={}&to={}&count={}&convertingPriceUnit={}'.format(
                    market, to, count, converting_price_unit)
            else:
                print(f'{market} => {to}보다 이전 일봉 데이터 조회')
                to = to.replace(' ', '%20').replace(':', '%3A')
                query = 'market={}&to={}&count={}'.format(market, to, count)
        else:
            if converting_price_unit:
                print(f'{market} => {converting_price_unit}로 환산하여 조회')
                query = 'market={}&count={}&convertingPriceUnit={}'.format(
                    market, count, converting_price_unit)
            else:
                query = 'market={}&count={}'.format(market, count)

        url = base_url + query

        # try - except
        res = rq.get(url, headers=self.headers).json()
        time.sleep(0.1)

        for i in range(len(res)):
            dict_row = res[i]
            df = df.append(dict_row, ignore_index=True)

        return df

    def get_week_candle(self, market='KRW-BTC', to=None, count=1) -> pd.DataFrame:
        """
        특정 화폐의 주봉 조회

        Parameters
        ----------
        market : string
            마켓 코드. 기본값은 KRW-BTC
        to : string
            마지막 캔들 시각(exclusive). 기본값은 None
            포맷 : yyyy-MM-dd HH:mm:ss
        count : int
            캔들 갯수. 기본값은 1. 최대 200개까지 요청 가능. 
        """

        df = pd.DataFrame()
        base_url = self.BASE_API_URL + '/candles/weeks?'

        if to:
            print(f'{market} => {to}보다 이전 주봉 데이터 조회')
            to = to.replace(' ', '%20').replace(':', '%3A')
            query = 'market={}&to={}&count={}'.format(market, to, count)
        else:
            query = 'market={}&count={}'.format(market, count)

        url = base_url + query

        # try - except
        res = rq.get(url, headers=self.headers).json()
        time.sleep(0.1)

        for i in range(len(res)):
            dict_row = res[i]
            df = df.append(dict_row, ignore_index=True)

        return df

    def get_month_candle(self, market='KRW-BTC', to=None, count=1) -> pd.DataFrame:
        """
        특정 화폐의 월봉 조회

        Parameters
        ----------
        market : string
            마켓 코드. 기본값은 KRW-BTC
        to : string
            마지막 캔들 시각(exclusive). 기본값은 None
            포맷 : yyyy-MM-dd HH:mm:ss
        count : int
            캔들 갯수. 기본값은 1. 최대 200개까지 요청 가능. 
        """

        df = pd.DataFrame()
        base_url = self.BASE_API_URL + '/candles/months?'

        if to:
            print(f'{market} => {to}보다 이전 월봉 데이터 조회')
            to = to.replace(' ', '%20').replace(':', '%3A')
            query = 'market={}&to={}&count={}'.format(market, to, count)
        else:
            query = 'market={}&count={}'.format(market, count)

        url = base_url + query

        # try - except
        res = rq.get(url, headers=self.headers).json()
        time.sleep(0.1)

        for i in range(len(res)):
            dict_row = res[i]
            df = df.append(dict_row, ignore_index=True)

        return df

    def get_transactions(self, market='KRW-BTC', to=None, count=1, cursor=None, days_ago=None):
        pass

    def get_ticker(self, market='KRW-BTC'):
        pass

    def get_orderbook(self, markets=['KRW-BTC']):

        df = pd.DataFrame()
        base_url = self.BASE_API_URL + '/orderbook?'

        if len(markets) > 1:
            params = '%2C%20'.join(markets)
            query = 'markets={}'.format(params)
        else:
            params = markets[0]
            query = 'markets={}'.format(params)

        url = base_url + query

        # try - except
        res = rq.get(url, headers=self.headers).json()
        time.sleep(0.1)

        for market_idx in range(len(res)):
            market_orderbook = res[market_idx]

            market = market_orderbook['market']
            timestamp = market_orderbook['timestamp']
            total_ask_size = market_orderbook['total_ask_size']
            total_bid_size = market_orderbook['total_bid_size']
            orderbook_units = market_orderbook['orderbook_units']

            temp_df = pd.DataFrame()

            for orderbook_units_idx in range(len(orderbook_units)):
                temp_df = temp_df.append(
                    orderbook_units[orderbook_units_idx], ignore_index=True)

            temp_df['market'] = market
            temp_df['timestamp'] = timestamp
            temp_df['total_ask_size'] = total_ask_size
            temp_df['total_bid_size'] = total_bid_size

            df = df.append(temp_df, ignore_index=True)
            df = df.reset_index(drop=True)

        return df


class WebsocketAPI(UpbitMachine):
    """
    업비트 API 중 Websocket과 관련된 API
    Websocket을 이용하여 수신할 수 있는 정보는 다음과 같다.
    1. 현재가(스냅샷, 실시간 정보 제공)
    2. 체결(스냅샷, 실시간 정보 제공)
    3. 호가(스냅샷, 실시간 정보 제공)

    스냅샷 정보는 요청 당시의 상태를 의미한다.
    실시간 정보는 요청 정보가 스트림 형태로 제공된다.

    요청은 JSON Object를 이용하며, 응답 또한 JSON Object다.
    요청의 형태는 아래와 같다.
    request = [
        {ticket field},
        {type field}, 
        {format field}
    ]

    Field
    -----
    1. Ticket Field
        용도를 식별하기 위해 ticket이라는 필드값이 필요하다.
        이 값은 시세를 수신하는 대상을 식별하며, 유니크한 값을 사용하도록 권장한다.(UUID 등)
    ticket : string
        식별값. 반드시 필요하다.

    2. Type Field
        수신하고 싶은 시세 정보를 나열하는 필드값이다. 
        isOnlySnapshot, isOnlyRealtime 필드는 생략가능하며 모두 생략시 스냅샷과 실시간
        데이터 모두를 수신한다.
        하나의 요청에 {type filed}는 여러 개를 명시할 수 있다.
    type : string
        수신할 시세 타입. 현재가(ticker), 체결(trade), 호가(orderbook)
    codes : list
        수신할 시세 종목. 대문자로 요청해야 함.
    isOnlySnapshot : Boolean
        시세 스냅샷만 제공
    isOnlyRealtime : Boolean
        실시간 시세만 제공

    3. Format Field
        Simple로 지정될 경우 응답의 필드명이 간소화됨. 
    format : string
        포맷. 

    """

    def __init__(self) -> None:
        super().__init__()
        self.BASE_WEBSOCKET_URL = 'wss://api.upbit.com/websocket/v1'
        self.subscribe_format = None

    def set_subscribe_format(self, *type_field, ticket_field='UNIQUE_TICKET', format_field=None):

        _ticket = {
            'ticket': ticket_field if ticket_field != 'test' else 'test '
        }
        if format_field:
            assert format_field != 'SIMPLE' 'Wrong format code'
            _format = {
                'format': format_field
            }

            subscribe_format = [
                _ticket,
                *type_field,
                _format
            ]
        else:
            subscribe_format = [
                _ticket,
                *type_field,
            ]

        self.subscribe_format = subscribe_format

    async def run_websocket(self):
        self.set_process()
        await self.subscribe_websocket()

    async def subscribe_websocket(self):
        async with websockets.connect(self.BASE_WEBSOCKET_URL) as ws:
            subscribe_data = json.dumps(self.subscribe_format)
            await ws.send(subscribe_data)

            while True:
                data = await ws.recv()
                data = json.loads(data)
                self.data_queue.put(data)

    def get_data(self):
        count = 0
        serial = 0
        df = pd.DataFrame()

        while not self.data_queue.empty():
            data = self.data_queue.get()
            if count == 1000:
                df.to_csv(self.DIR_DATABASE + '\\data_{}.csv'.format(serial))
                serial += 1
                df = pd.DataFrame()
                count = 0
            df = df.append(data, ignore_index=True)
            count += 1
            print(count)
            self.data_queue.task_done()

    def set_process(self):
        self.proc = Process(target=self.get_data, name='Data Consumer')

    def run_process(self):
        self.proc.start()


class UpbitAPIException(Exception):
    pass
