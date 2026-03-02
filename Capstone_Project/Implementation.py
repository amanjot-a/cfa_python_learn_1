import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# --- Amazon data ---
stock_df = pd.read_csv('Capstone_Project/Amazon.csv')
stock_df['Daily Return'] = stock_df['Adj Close'].pct_change(1) * 100
stock_df['Daily Return'].replace(np.nan, 0, inplace=True)
print('Amazon head:')
print(stock_df.head())
print('Amazon describe:')
print(stock_df.describe().round(2))

# --- JPMorgan data ---
JPM_df = pd.read_csv('Capstone_Project/JPM.csv')
JPM_df['Daily Return'] = JPM_df['Adj Close'].pct_change(1) * 100
JPM_df['Daily Return'].replace(np.nan, 0, inplace=True)

print('\nJPM head:')
print(JPM_df.head())
print('\nNulls count for JPM:')
print(JPM_df.isnull().sum())
print('Memory usage bytes:', JPM_df.memory_usage(deep=True).sum())
print('Max JPM daily return:', JPM_df['Daily Return'].max())

# classification function

def percentage_return_classifier(pct):
    if pct > -0.3 and pct <= 0.3:
        return 'Insignificant Change'
    elif pct > 0.3 and pct <= 3:
        return 'Positive Change'
    elif pct > -3 and pct <= -0.3:
        return 'Negative Change'
    elif pct > 3 and pct <= 7:
        return 'Large Positive Change'
    elif pct > -7 and pct <= -3:
        return 'Large Negative Change'
    elif pct > 7:
        return 'Bull Run'
    elif pct <= -7:
        return 'Bear Sell Off'

JPM_df['Trend'] = JPM_df['Daily Return'].apply(percentage_return_classifier)
trend_summary = JPM_df['Trend'].value_counts()
print('\nJPM trend summary:')
print(trend_summary)

# optional: plot pie chart
plt.figure(figsize=(8,8))
trend_summary.plot(kind='pie', y='Trend', autopct='%1.1f%%', startangle=90)
plt.ylabel('')
plt.title('JPM % Daily Return Classification')
plt.savefig('Capstone_Project/jpm_trend_pie.png')
print('\nSaved pie chart to Capstone_Project/jpm_trend_pie.png')

# Quick plotly example (will open interactive windows if run in notebook)
# Commented out for script
# plot_financial_data omitted

print('\nScript complete.')
