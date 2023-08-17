# 원화거래 / BTC 거래 / USDT 거래
# 1.업비트의 코인 종류 체크

from urllib.parse import urlencode
import hashlib
import uuid
import jwt
import os
import pandas as pd
import time
import requests
import json


def coins(current):
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails": "true"}
    response = requests.request("GET", url, params=querystring)
    response_json = json.loads(response.text)

    KRWticker = []
    BTCticker = []
    USDTticker = []

    for a in response_json:
        #     print(a['market'])
        if "KRW-" in a['market']:
            KRWticker.append(a['market'])
        elif "BTC-" in a['market']:
            BTCticker.append(a['market'])
        elif "USDT-" in a['market']:
            USDTticker.append(a['market'])
    ticker = {
        "KRW": KRWticker,
        "BTC": BTCticker,
        "USDT": USDTticker
    }
#     print(ticker)
    if current == "ALL":
        ticker = ticker
    else:
        ticker = ticker[current]
    return ticker


# 암호화폐 시세조회


def coin_price(coin):
    url = "https://api.upbit.com/v1/orderbook"
    querystring = {"markets": coin}
    response = requests.request("GET", url, params=querystring)
    response_json = json.loads(response.text)
    coin_now_price = response_json[0]["orderbook_units"][0]["ask_price"]
    return coin_now_price
# 시세 호가 정보(Orderbook) 조회 // 호가 정보 조회


def coin_history(coin, time1='minute', time2=""):
    url = f"https://api.upbit.com/v1/candles/{time1}/{time2}"

    querystring = {"market": coin, "count": "200"}

    response = requests.request("GET", url, params=querystring)
    response_json = json.loads(response.text)
    # print(type(response_json))
    df = pd.DataFrame(response_json)
    return df

# 로그인


def login():
    global access_key
    global secret_key
    access_key = input("access_key : ")
    secret_key = input("secret_key : ")


# 나의 계좌 잔액 조회


def balance():
    global server_url
    server_url = 'https://api.upbit.com'

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)
    return res.json()


# 매수(지정가)


# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

def buy_limit(coin, volume, price):
    query = {
        'market': coin,
        'side': 'bid',
        'volume': volume,
        'price': price,
        'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders",
                        params=query, headers=headers)
    print(res.json())
    return res.json()


# 매수(시장가)


# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

def buy_market(coin, price):
    query = {
        'market': coin,
        'side': 'bid',
        'volume': '',
        'price': price,
        'ord_type': 'price',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders",
                        params=query, headers=headers)
    print(res.json())
    return res.json()


# 매도(지정가)


# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

def sell_limit(coin, volume, price):
    query = {
        'market': coin,
        'side': 'ask',
        'volume': volume,
        'price': price,
        'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders",
                        params=query, headers=headers)
    print(res.json())
    return res.json()

# 매도(시장가)


# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

def sell_market(coin, volume):
    query = {
        'market': coin,
        'side': 'ask',
        'volume': volume,
        'price': '',
        'ord_type': 'market',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders",
                        params=query, headers=headers)
    print(res.json())
    return res.json()


login()


def price_trim(price_trim):

    # ~10원 미만[소수점 둘째자리]
    if price_trim < 10:
        price_trim = round(price_trim, 2)

    # 10~100원 미만 - [소수점첫째자리]
    elif price_trim < 100:
        price_trim = round(price_trim, 1)

    # 100~1,000원 미만 - [1원단위]
    elif price_trim < 1000:
        price_trim = round(price_trim)

    # 1,000~10,000원 미만[5원단위]
    elif price_trim < 10000:
        price_trim = round(price_trim*2, -1)/2

    # 10,000~100,000원 미만[10원단위]
    elif price_trim < 100000:
        price_trim = round(price_trim, -1)

    # 100,000~500,000원 미만 [50원단위]
    elif price_trim < 500000:
        price_trim = round(price_trim*2, -2)/2

    # 500,000원~1,000,000원 미만[100원단위]
    elif price_trim < 1000000:
        price_trim = round(price_trim, -2)

    # 1,000,000~2,000,000 [500원단위]
    elif price_trim < 2000000:
        price_trim = round(price_trim*2, -3)/2

    # 2,000,000 이상 [1000원단위]
    else:
        price_trim = round(price_trim, -3)

    return price_trim


print("진행9")

while True:
    try:
        # n분봉으로 최근 n분 동안 가장 높은 상승률을 보인 코인 찾기
        n = 10  # 원하는 n 값으로 설정
        tickers = coins("KRW")
        increase_top_score = 0
        increase_top_score_ticker = None
        print("진행10")
        
        for ticker in tickers:
            time.sleep(1) 
            coin_n_m = coin_history(ticker, 'minutes', n)
            
            min_start_price = coin_n_m["opening_price"].min()
            now_price = coin_price(ticker)
            increase_percent = round(((now_price / min_start_price - 1) * 100), 3)
            
            if increase_percent > increase_top_score:
                increase_top_score = increase_percent
                increase_top_score_ticker = ticker
        
        print(increase_top_score_ticker)
        
        if increase_top_score_ticker is not None:
            # 해당 코인을 시장가에 구매
            balance_info = balance()
            for a in balance_info:
                if a['currency'] == 'KRW':
                    buy_amount = float(a['balance']) * 0.10
                    buy_market(increase_top_score_ticker, buy_amount)
                    time.sleep(3)
        
            # 10분간 감시
            time_elapsed = 0
            while time_elapsed < 600:
                time.sleep(60)  # 60초마다 상태 감시
                
                coin_10_m = coin_history(increase_top_score_ticker, 'minutes', 20)
                max_price_10_m = coin_10_m["high_price"].max()
                current_price = coin_price(increase_top_score_ticker)
                decrease_percent_10_m = round(((1 - current_price / max_price_10_m) * 100), 3)
                
                if decrease_percent_10_m >= 0 or current_price <= buy_amount:
                    # 구매 가격에 도달하거나 20분간 하락한 경우 매도
                    sell_limit_price = price_trim(current_price * 0.98)  # 구매 가격의 98%
                    balance_info = balance()
                    for a in balance_info:
                        if a['currency'] == increase_top_score_ticker.replace("KRW-", ""):
                            sell_balance = a['balance']
                            sell_limit(increase_top_score_ticker, sell_balance, sell_limit_price)
                            print("매도 완료")
                            break
                    break
                
                time_elapsed += 60  # 60초마다 경과 시간 증가
        
        time.sleep(10)
        
    except:
        print("에러 발생, 재시작합니다.")
        time.sleep(10)
