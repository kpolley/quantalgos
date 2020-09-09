import time
import datetime
import alpaca_trade_api as tradeapi

import credentials
from MACD import MACD

APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

STOCKS = ["WM", "AAPL", "CCL", "V", "TWTR", "NVDA"]

alpaca = tradeapi.REST(credentials.alpaca_key_id, credentials.alpaca_secret_key, APCA_API_BASE_URL, 'v2')

def awaitMarketOpen():
    while not alpaca.get_clock().is_open:
        next_open = alpaca.get_clock().next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
        current_time = alpaca.get_clock().timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        time_until_open = int((next_open - current_time) / 60)
        print(f"After hours. Next open in {time_until_open} seconds")
        time.sleep(time_until_open + 60)
def main():
    runners = [MACD(stock, 10, alpaca) for stock in STOCKS]

    while True:
        try:
            awaitMarketOpen()
            for runner in runners:
                runner.run()
            time.sleep(60)
        except ConnectionError as e:
            print(f"connection error: {e}")

if __name__ == "__main__":
    main()