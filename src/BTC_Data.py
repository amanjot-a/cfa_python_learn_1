import yfinance as yf
import pandas as pd
from tabulate import tabulate

BTC_data = yf.Ticker("BTC-USD")
Meta_data = yf.Ticker("META")
Apple_data = yf.Ticker("AAPL")
Spotify_data = yf.Ticker("SPOT")
P_G_data = yf.Ticker("PG")


print(BTC_data)

BTC_data_history = BTC_data.history(period="10d")
print(BTC_data_history)
print(" ")
print("Total Circulating Supply of Bitcoin is = {}".format(BTC_data.info['circulatingSupply']))
print(" ")

print("The Beta of Meta Stock is = {}".format(Meta_data.info['beta']))
print("The Beta of Apple Stock is = {}".format(Apple_data.info['beta']))
print("The Beta of Spotify Stock is = {}".format(Spotify_data.info['beta']))
print("The Beta of P&G Stock is = {}".format(P_G_data.info['beta']))

print("The Volume of Apple Stock Transactions on 2022/02/22 is = {}".format(Apple_data.history(start="2022-02-22", end="2022-02-23")['Volume'][0]))
