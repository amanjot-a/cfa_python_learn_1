# This code uses the yfinance library to retrieve historical stock data for Apple Inc. and displays it in a tabular format using the tabulate library.
# The yfinance library allows us to access financial data from Yahoo Finance, and the tabulate library helps us format the output in a more readable way. The code retrieves the historical data for Apple Inc. over the past 10 years and prints it in a fancy grid format.

import yfinance as yf
import pandas as pd     
from tabulate import tabulate
pd.set_option('display.float_format', '{:.2f}'.format)

Apple_stock = yf.Ticker("AAPL")
# The code above uses the yfinance library to create a Ticker object for Apple Inc.

print(Apple_stock)
# The info attribute of the Ticker object provides a dictionary containing various details about the stock, such as its current price, market capitalization, and other financial information.

Apple_stock_history = Apple_stock.history(period="10d")
# The history() method is used to retrieve historical market data for the stock. The period="10d" argument specifies that we want to retrieve data for the past 10 days.


print(Apple_stock_history )


print("The company beta is = {}".format(Apple_stock.info['beta']))

print("The comapany market cap is = {}".format(Apple_stock.info['marketCap']))

print("the Comapny Cash on hand is = {}".format(Apple_stock.info['freeCashflow']))

print("The company Price-to-Earnings (P/E) ratio is = {} ".format(Apple_stock.info['trailingPE']))


balance_sheet = Apple_stock.get_balance_sheet()
income_statement = Apple_stock.get_income_stmt()
cash_flow = Apple_stock.get_cashflow()  

print(balance_sheet)
print(income_statement)
print(cash_flow)