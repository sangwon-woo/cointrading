from abc import ABC, abstractmethod

class Machine(ABC):
    @abstractmethod
    def get_filled_orders(self):
        """체결정보룰 구하는 메서드
        """
        pass

    @abstractmethod
    def get_wallet_status(self):
        """사용자의 지갑정보를 조회하는 메서드
        """
        pass

    @abstractmethod
    def get_token(self):
        """액세스 토큰 정보를 구하는 메서드
        """
        pass

    @abstractmethod
    def set_token(self):
        """액세스 토큰 정보를 만드는 메서드
        """
        pass

    @abstractmethod
    def get_username(self):
        """현재 사용자 이름을 구하는 메서드
        """
        pass

    @abstractmethod
    def buy_order(self):
        """매수주문을 실행하는 메서드
        """
        pass

    @abstractmethod
    def sell_order(self):
        """매도주문을 실행하는 메서드
        """
        pass

    @abstractmethod
    def cancel_order(self):
        """취소주문을 실행하는 메서드
        """
        pass

    @abstractmethod
    def get_my_order_status(self):
        """사용자의 주문 상세 정보를 조회하는 메서드
        """
        pass

    
