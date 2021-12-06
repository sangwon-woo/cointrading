import jwt
import uuid
import hashlib
import requests
import pprint
from urllib.parse import urlencode
from config.setting import *

server_url = 'https://api.upbit.com'

query = {
    'market' : 'KRW-ETH'
}
query_string = urlencode(query).encode()

m = hashlib.sha512()
m.update(query_string)
query_hash = m.hexdigest()

payload = {
    'access_key' : UPBIT_ACCESS_KEY,
    'nonce' : str(uuid.uuid4()),
    'query_hash' : query_hash,
    'query_hash_alg' : 'SHA512'
}

jwt_token = jwt.encode(payload, UPBIT_SECRET_KEY)
authorization_token = 'Bearer {}'.format(jwt_token)
headers = {'Authorization' : authorization_token}

res = requests.get(
    server_url + '/v1/orders/chance',
    params=query,
    headers=headers
).json()

pprint.pprint(res)