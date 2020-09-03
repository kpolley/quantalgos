import alpaca_trade_api as tradeapi
import pandas as pd 
import numpy as np

class MACD:
    def __init__(self, stock, quantity, alpaca):
        self.stock = stock
        self.alpaca = alpaca
        self.quantity = quantity
        self.holding = False

    def submitOrder(self, qty, stock, side):
        if qty == 0:
            print("Quantity is 0, order of | " + str(qty) + " " + stock + " " + side + " | not completed.")
            return

        try:
            self.alpaca.submit_order(stock, qty, side, "market", "day")
            print("Market order of | " + str(qty) + " " + stock + " " + side + " | completed.")
        except Exception as e:
            print("Order of | " + str(qty) + " " + stock + " " + side + " | did not go through.")
            print(e)


    def run(self):
        last_hour = self.alpaca.get_barset(self.stock, "minute", 60)
        last_hour = pd.Series([x.c for x in last_hour[self.stock]])

        long_ema = pd.Series.ewm(last_hour, span=26).mean().iloc[-1]
        short_ema = pd.Series.ewm(last_hour, span=12).mean().iloc[-1]

        macd = long_ema - short_ema
        
        print(f"{self.stock} : {macd} | Holding: {self.holding}")

        if macd > 0.1 and not self.holding:
            self.submitOrder(self.quantity, self.stock, "buy")
            self.holding = True
        elif macd < -0.1 and self.holding:
            self.submitOrder(self.quantity, self.stock, "sell")
            self.holding = False
        # else: do nothing