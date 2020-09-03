import time
import datetime
import alpaca_trade_api as tradeapi

import credentials
from MACD import MACD

APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

STOCKS = ["WM", "AAPL", "CCL", "V", "TWTR", "NVDA"]

alpaca = tradeapi.REST(credentials.alpaca_key_id, credentials.alpaca_secret_key, APCA_API_BASE_URL, 'v2')

MARKET_OPEN = datetime.time(9,0)
MARKET_CLOSED = datetime.time(13,0)

def awaitMarketOpen():
    this_hour = datetime.datetime.now().time()
    while this_hour <= MARKET_OPEN or this_hour >= MARKET_CLOSED:
        print("After hours")
        time.sleep(60)

def main():
    runners = [MACD(stock, 10, alpaca) for stock in STOCKS]

    while True:
        awaitMarketOpen()
        for runner in runners:
            runner.run()
        time.sleep(60)

if __name__ == "__main__":
    main()