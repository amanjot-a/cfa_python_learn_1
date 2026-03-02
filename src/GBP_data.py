import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

GDP_df = pd.DataFrame({
    'Country': ['USA', 'China', 'Japan', 'Germany', 'India'],  
    'Country Code': ['US', 'CN', 'JP', 'DE', 'IN'],
    'GDP per Capita': [65000, 10000, 40000, 45000, 2000],
    'Global Rank': [5, 64, 27, 19, 142]})

# print(GDP_df)
#  # This will print the entire DataFrame to the console.

# print(GDP_df.tail(1))
#  # if we want to see the last row of the DataFrame, we can use the tail() method with an argument of 1.

# print(GDP_df['GDP per Capita'])
#  # If we need data from a specific column, we can use the column name as an index.

# print(GDP_df.describe()) 
#  # To get a statistical summary of the numerical columns in the DataFrame, we can use the describe() method.

# print(GDP_df.info())
#     # To get information about the DataFrame, including the data types of each column and the number of non-null entries, we can use the info() method.



# Practise Solution 4.1 #

portfolio_df = pd.DataFrame({
    'Stock': ['HDFC Bank', 'Reliance Industries', 'Tata Consultancy Services', 'Infosys', 'ICICI Bank'],
    'Sector': ['Banking', 'Energy', 'IT', 'IT', 'Banking'],
    'Number of Shares': [100, 50, 30, 80, 120],
    'Ticker Symbol': ['HDFCBANK', 'RELIANCE', 'TCS', 'INFY', 'ICICIBANK'],
    'Current Market Price': [900, 400, 2000, 1500, 700]})

#print(portfolio_df)
# Simplely printing the DataFrame will show the data in a tabular format, but it may not be very visually appealing.

print(tabulate(portfolio_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# To make the DataFrame more visually appealing when printed, we can use the tabulate library to format it as a grid.

print(tabulate(portfolio_df.describe(), headers='keys', tablefmt='grid'))

portfolio_df['Portfolio Value'] = portfolio_df['Number of Shares'] * portfolio_df['Current Market Price']
print(tabulate(portfolio_df, headers='keys', tablefmt='grid'))

print('total portfolio value is', portfolio_df['Portfolio Value'].sum())