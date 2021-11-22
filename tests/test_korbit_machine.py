import unittest
from unittest import async_case
from autotrading.machine.korbit_machine import KorbitMachine
import inspect

class KorbitMachineTestCase(unittest.TestCase):

    def __init__(self):
        self.korbit_machine = KorbitMachine()

    def tearDown(self):
        pass
    
    def test_set_token(self):
        print(inspect.stack()[0][3])
        expire, access_token, refresh_token = self.korbit_machine.set_token(grant_type='password')
        assert access_token
        print('Expire:', expire, 'Access token:', access_token, 'Refresh token', refresh_token)


if __name__ == '__main__':
    print(__name__)
    c = KorbitMachineTestCase()
    c.test_set_token()